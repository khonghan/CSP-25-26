#include "include.cpp"
using namespace std;

// different screens
enum class gameState {
    MENU,
    ACTIVE_TEST,
    TEST_OPTIONS,
    RESULTS,
    SETTINGS
};

// different test types
enum class testType {
    TIME,
    WORDS,
    CUSTOM
};

// holds game stats, allows tracking and updating stats during the test
struct gameStats {
    int totalChars = 0;
    int correctChars = 0;
    int incorrectChars = 0;
    int totalWords = 0;
    double accuracy = 0.0;
    double rawWPM = 0.0;
    double netWPM = 0.0;
    double timeTaken = 0.0; // seconds

    string userInput;
    string targetText;
    vector<bool> characterStatus; // track (in)correct characters

    void calculateStats(double elapsedTime){
        timeTaken = elapsedTime;

        // recompute totals from the provided userInput/characterStatus so backspaces are reflected immediately
        int computedTotal = static_cast<int>(userInput.length());
        int computedCorrect = 0;
        for(int i = 0; i < computedTotal; ++i){
            if(i < static_cast<int>(characterStatus.size()) && characterStatus[i]) computedCorrect++;
        }
        int computedIncorrect = max(0, computedTotal - computedCorrect);

        totalChars = computedTotal;
        correctChars = computedCorrect;
        incorrectChars = computedIncorrect;

        // if total characters > 0, then calculate accuracy percentage
        accuracy = (totalChars > 0) ? (static_cast<double>(correctChars) / totalChars) * 100.0 : 0.0;

        if(elapsedTime > 0){
            double minutes = elapsedTime / 60.0;

            rawWPM = (minutes > 0) ? (static_cast<double>(totalChars) / 5.0) / minutes : 0.0;

            // error penalty in words per minute
            double errorPenalty = (minutes > 0) ? (static_cast<double>(incorrectChars) / 5.0) / minutes : 0.0;

            // net WPM: raw minus penalty
            netWPM = rawWPM - errorPenalty;
            if(netWPM < 0) netWPM = 0;
        }
    }
};

struct gameSettings{
    testType testMode = testType::WORDS;
    int wordCount = 10;
    int timeLimit = 30; // seconds for time mode
    string customText = "";
    bool includePunctuation = false;
    bool includeNumbers = false;
};

class textGenerator {
private:
    vector<string> wordList;

public:
    textGenerator(){
        srand(static_cast<unsigned int>(time(0)));
    }

    // load words from file into wordList
    bool generateWordList(const string& filename){
        ifstream file(filename);
        if(!file.is_open()){
            cerr << RED << "Error opening word list file: " << filename << RESET << endl;
            return false;
        }

        string word;
        wordList.clear();

        while(file >> word){
            // filter out non-alphabetic words
            if(all_of(word.begin(), word.end(), ::isalpha)){
                transform(word.begin(), word.end(), word.begin(), ::tolower);
                wordList.push_back(word);
            }
        }

        file.close();

        if(wordList.empty()){
            cerr << RED << "Error: Word list is empty/invalid." << RESET << endl;
            return false;
        }

        cout << GREEN << "Loaded " << wordList.size() << " words successfully!" << RESET << endl;
        return true;
    }

    string getRandomWord(){
        if(wordList.empty()) return "error";
        return wordList[rand() % wordList.size()];
    }

    string generateText(int wordCount, const gameSettings& settings){
        string result;
        
        // iterate a specified # of words
        for(int i = 0; i < wordCount; i++){
            string word = getRandomWord();

            // add numbers if enabled in settings
            if(settings.includeNumbers && (rand() % 5 ==0)){
                word += to_string(rand() % 100);
            }

            result += word;

            // add space between words
            if(i < wordCount - 1){
                result += " ";
            }

            // add punctuation if enabled in settings
            if (settings.includePunctuation && (rand() % 8 == 0) && i < wordCount - 1){
                char punctuation[] = {'.', ',', '!', '?'};
                result += punctuation[rand() % 4];
                result += " ";
            }
        }

        return result;
    }

    bool isLoaded() const{
        return !wordList.empty();
    }

    int getWordCount() const{
        return wordList.size();
    }
};

class typingGame{
private:
    gameState currentState;
    gameSettings settings;
    gameStats stats;
    textGenerator textGen;

    string targetText;
    string userInput;
    vector<bool> characterStatus; // track (in)correct characters

    chrono::steady_clock::time_point testStartTime;
    bool testStarted;
    double elapsedTime;

public:
    typingGame() : currentState(gameState::MENU), testStarted(false), elapsedTime(0.0){}

    // raii guard for enabling/disabling terminal raw mode
    struct TermiosGuard {
        struct termios orig{};
        bool valid = false;
        TermiosGuard(){ if(tcgetattr(STDIN_FILENO, &orig) == 0) valid = true; }
        void enableRaw(){
            if(!valid) return;
            struct termios raw = orig;
            raw.c_lflag &= ~(ECHO | ICANON | ISIG);
            raw.c_iflag &= ~(IXON | ICRNL);
            raw.c_cc[VMIN] = 1;
            raw.c_cc[VTIME] = 0;
            tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
        }
        void restore(){ if(valid) tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig); }
        ~TermiosGuard(){ restore(); }
    };

    // init game (load word list)
    bool init(){
        if(!textGen.generateWordList("1000-most-common-words.txt")){
            cerr << RED << "Failed to load word list!" << RESET << endl;
            cerr << "Please ensure '1000-most-common-words.txt' file exists in the same directory." << endl;
            return false;
        }

        return true;
    }

    // clear screen across platforms
    void clearScreen(){
        #ifdef _WIN32
            system("cls");
        #else
            system("clear");
        #endif
    }

    void printHeader(){
        cout << CYAN << BOLD;
        cout << "╔════════════════════════════════════════════════════════════╗" << endl;
        cout << "║                   SUPER COOL TYPING TEST                   ║" << endl;
        cout << "╚════════════════════════════════════════════════════════════╝" << RESET << endl;
        cout << endl;
    }

    void startTest(){
        clearScreen();

        // reset game state
        userInput.clear();
        stats = gameStats();
        testStarted = false;
        elapsedTime = 0.0;

        // generate text based on test mode
        switch(settings.testMode){
            case testType::WORDS:
                targetText = textGen.generateText(settings.wordCount, settings);
                break;
                
            case testType::TIME:{
                // generate a text sufficiently long for time mode
                // estimate words based on time limit (approx 2 words per second)
                    int wordEstimate = max(30, settings.timeLimit * 2);
                    targetText = textGen.generateText(wordEstimate, settings);
                }
                break;

            case testType::CUSTOM:
                targetText = settings.customText;
                if(targetText.empty()){
                    cout << RED << "No custom text. Returning to menu..." << RESET << endl;
                    cin.get();
                    currentState = gameState::MENU;
                    return;
                }
                break;
        }

        characterStatus.clear();
        characterStatus.resize(targetText.length(), false);

        currentState = gameState::ACTIVE_TEST;

        cout << YELLOW << "Test starting with " << targetText.length() << " characters..." << RESET << endl;
        cout << endl;
    }

    // process typed character
    void processCharacter(char c){
        // start timer when user first inputs
        if(!testStarted){
            testStarted = true;
            testStartTime = chrono::steady_clock::now();
        }

        userInput += c;
        size_t idx = userInput.length() - 1;

        stats.totalChars++;

        // if character is (in)correct
        if(idx < targetText.length() && userInput[idx] == targetText[idx]){
            characterStatus[idx] = true;
            stats.correctChars++;
        } else {
            stats.incorrectChars++;
        }

        // if test is complete
        if(userInput.length() >= targetText.length()){
            finishTest();
        }
    }

    // calculate elapsed time
    void updateTimer(){
        if(testStarted && currentState == gameState::ACTIVE_TEST){
            auto now = chrono::steady_clock::now();
            elapsedTime = chrono::duration<double>(now - testStartTime).count();

            // time limit for time mode
            if(settings.testMode == testType::TIME && elapsedTime >= settings.timeLimit){
                finishTest();
            }
        }
    }

    void finishTest(){
        currentState = gameState::RESULTS;
        // provide current typed/target data to stats for accurate calculation
        stats.userInput = userInput;
        stats.targetText = targetText;
        stats.characterStatus = characterStatus;
        stats.calculateStats(elapsedTime);

        // count words
        int targetWords = 1;
        for(char c : targetText){
            if(c == ' ') targetWords++;
        }
        stats.totalWords = targetWords;
    }

    void displayColorText(){
        for(size_t i = 0; i < targetText.length(); i++){
            if(i < userInput.length()){
                // typed characters
                if(characterStatus[i]){
                    cout << GREEN << targetText[i] << RESET; // correct character
                } else {
                    cout << RED << targetText[i] << RESET; // incorrect character
                }
            } else if(i == userInput.length()){
                // current character
                cout << YELLOW << BOLD << targetText[i] << RESET;
            } else {
                cout << GRAY << targetText[i] << RESET;
            }
        }
        cout << endl;
    }

    void showMenu(){
        clearScreen();
        printHeader();

        cout << "Welcome! Test your typing speed and accuracy." << endl;
        cout << endl;

        cout << BOLD << "MENU OPTIONS:" << RESET << endl;
        cout << " [1] Test Options" << endl;
        cout << " [2] Settings" << endl;
        cout << " [3] Exit" << endl;
        cout << endl;

        cout << CYAN << "Current Mode: ";
        switch(settings.testMode){
            case testType::WORDS:
                cout << settings.wordCount << " words";
                break;
            case testType::TIME:
                cout << settings.timeLimit << " seconds";
                break;
            case testType::CUSTOM:
                cout << "Custom Text";
                break;
        }

        cout << RESET << endl;
        cout << endl;

        cout << "Enter your choice: ";
    }

    void showTestOptions(){
        clearScreen();

        cout << BOLD << "╔════════════════════════════════════════════════════════════╗" << endl;
        cout << "║                      TEST OPTIONS                          ║" << endl;
        cout << "╚════════════════════════════════════════════════════════════╝" << RESET << endl;
        cout << endl;

        cout << CYAN << "Choose your test type:" << RESET << endl;
        cout << endl;

        // test type WORDS
        cout << BOLD << "[1] Words Mode" << RESET << endl;
        cout << endl;

        // test type TIME
        cout << BOLD << "[2] Time Mode" << RESET << endl;
        cout << endl;

        // test type CUSTOM
        cout << BOLD << "[3] Custom Mode" << RESET << endl;
        cout << endl;

        cout << "[4] Return to Menu" << endl;
        cout << endl;

        cout << "Enter your choice (1-4): ";
    }

    void handleTestOptions(const string& choice){
        if(choice == "1"){ // WORDS
            clearScreen();
            // printHeader();

            cout << BOLD << "WORDS MODE" << RESET << endl;
            cout << endl;
            cout << "  [a] 10 words" << endl;
            cout << "  [b] 25 words" << endl;
            cout << "  [c] 50 words" << endl;
            cout << "  [d] 100 words" << endl;
            cout << "  [e] Custom word count" << endl;
            cout << endl;
            cout << "Choice: ";

            string subchoice;
            getline(cin, subchoice);

            settings.testMode = testType::WORDS;

            if(subchoice == "a"){
                settings.wordCount = 10;
            } else if(subchoice == "b"){
                settings.wordCount = 25;
            } else if(subchoice == "c"){
                settings.wordCount = 50;
            } else if(subchoice == "d"){
                settings.wordCount = 100;
            } else if(subchoice == "e"){
                int custom;
                while(true){
                    cout << "Enter custom word count (1-500): ";
                    string line;
                    getline(cin, line);

                    if(line.empty()){
                        // if the user just pressed enter, prompt again
                        continue;
                    }

                    stringstream ss(line);
                    if(!(ss >> custom) || !(ss.eof())){
                        cout << RED << "Invalid input. Please enter a valid integer." << RESET << endl;
                        continue;
                    }

                    if(custom > 0 && custom <= 500){
                        settings.wordCount = custom;
                        break;
                    } else {
                        cout << RED << "Please enter an integer between 1 and 500." << RESET << endl;
                    }
                }
            }

            // if subchoice wasn't recognized, inform user and return to options
            if(subchoice != "a" && subchoice != "b" && subchoice != "c" && subchoice != "d" && subchoice != "e"){
                cout << RED << "Invalid choice. Valid: a, b, c, d, e. Press Enter to continue..." << RESET << endl;
                cin.get();
                currentState = gameState::TEST_OPTIONS;
                return;
            }

            cout << GREEN << "Set to " << settings.wordCount << " words mode!" << RESET << endl;
            cout << "Press Enter to start test...";
            cin.get();
            startTest();

        } else if(choice == "2"){
            clearScreen();
            // printHeader();

            cout << BOLD << "TIME MODE" << RESET << endl;
            cout << endl;
            cout << "  [a] 15 seconds" << endl;
            cout << "  [b] 30 seconds" << endl;
            cout << "  [c] 60 seconds" << endl;
            cout << "  [d] 120 seconds" << endl;

            string subchoice;
            getline(cin, subchoice);

            settings.testMode = testType::TIME;

            if(subchoice == "a"){
                settings.timeLimit = 15;
            } else if(subchoice == "b"){
                settings.timeLimit = 30;
            } else if(subchoice == "c"){
                settings.timeLimit = 60;
            } else if(subchoice == "d"){
                settings.timeLimit = 120;
            } else {
                cout << RED << "Invalid choice. Valid: a, b, c, d. Press Enter to continue..." << RESET << endl;
                cin.get();
                currentState = gameState::TEST_OPTIONS;
                return;
            }

            cout << GREEN << "Set to " << settings.timeLimit << " seconds mode!" << RESET << endl;
            cout << "Press Enter to start test...";
            cin.get();
            startTest();

        } else if(choice == "3"){
            clearScreen();
            // printHeader();

            cout << BOLD << "CUSTOM MODE" << RESET << endl;
            cout << endl;
            cout << "Enter your custom text (press Enter when done):" << endl;
            cout << CYAN << "> " << RESET;

            settings.testMode = testType::CUSTOM;

            while(true){
                getline(cin, settings.customText);
                if(settings.customText.empty()){
                    cerr << RED << "Custom text is empty. Please enter something for custom text." << RESET << endl;
                    cout << CYAN << "> " << RESET;
                    continue;
                }
                break;
            }

            cout << GREEN << "Custom text set!" << RESET << endl;
            cout << "Press Enter to start test...";
            cin.get();
            startTest();

        } else if(choice == "4"){
            currentState = gameState::MENU;
        } else {
            cout << RED << "Invalid option. Please select an integer 1-4. Press Enter to continue..." << RESET << endl;
            cin.get();
            currentState = gameState::TEST_OPTIONS;
        }
    }

    void showTest(){
        clearScreen();
        // printHeader();

        updateTimer();

        cout << BOLD;
        if(settings.testMode == testType::TIME){
            double timeRemaining = settings.timeLimit - elapsedTime;
            if(timeRemaining < 0) timeRemaining = 0;
            cout << "TIME REMAINING: " << fixed << setprecision(1)
                      << timeRemaining << "s / " << settings.timeLimit << "s" << RESET << endl;
        } else {
            cout << "TIME: " << fixed << setprecision(1)
                      << elapsedTime << "s" << RESET << endl;
        }

        cout << "Progress: " << userInput.length() << " / " << targetText.length() << " characters (" 
                  << (int)((float)userInput.length() / targetText.length() * 100) << "%)" << endl;

        cout << "Correct: " << GREEN << stats.correctChars << RESET
                  << " | Incorrect: " << RED << stats.incorrectChars << RESET << endl;
        
        cout << endl;

        cout << "─────────────────────────────────────────────────────────" << endl;
        cout << BOLD << "TYPE THIS:" << RESET << endl;
        cout << endl;

        displayColorText();

        cout << endl;
        cout << "─────────────────────────────────────────────────────────" << endl;
        cout << endl;

        cout << BOLD << "YOUR INPUT:" RESET << endl;
        cout << userInput << endl;
        cout << endl;

        cout << GRAY << "(Type the text above. Press ESC to cancel)" << RESET << endl;
    }

    void showResults(){
        clearScreen();

        cout << GREEN << BOLD << "╔════════════════════════════════════════════════════════════╗" << endl;
        cout << "║                     TEST COMPLETE!                         ║" << endl;
        cout << "╚════════════════════════════════════════════════════════════╝" << RESET << endl;
        cout << endl;

        cout << CYAN << BOLD << "PERFORMANCE SUMMARY:" << RESET << endl;
        cout << "─────────────────────────────────────────────────────────" << endl;
        cout << endl;

        cout << "Time Taken: " YELLOW << fixed << setprecision(2)
                  << stats.timeTaken << " seconds" << RESET << endl;
        cout << endl;

        cout << BOLD << "Speed:" << RESET << endl;
        cout << " Raw WPM: " << MAGENTA << fixed << setprecision(1)
                  << stats.rawWPM << RESET << endl;
        cout << " Net WPM: " << MAGENTA << BOLD << stats.netWPM << RESET << endl;
        cout << endl;

        cout << BOLD << "Accuracy:" << RESET << endl;
        cout << " Overall: ";
        if(stats.accuracy >=90) cout << GREEN;
        else if(stats.accuracy >= 80) cout << YELLOW;
        else cout << RED;
        cout << BOLD << stats.accuracy << "%" << RESET << endl;
        cout << endl;

        cout << BOLD << "Character Stats:" << RESET << endl;
        cout << " Total: " << stats.totalChars << endl;
        cout << "  Correct: " << GREEN << stats.correctChars << RESET << endl;
        cout << "  Incorrect: " << RED << stats.incorrectChars << RESET << endl;
        cout << endl;

        cout << "─────────────────────────────────────────────────────────" << endl;
        cout << endl;

        cout << "Press [1] to try again, [2] for menu: ";
    }

    void showSettings(){
        clearScreen();
        // printHeader();

        cout << BOLD << "GENERAL SETTINGS" << RESET << endl;
        cout << "─────────────────────────────────────────────────────────" << endl;
        cout << endl;

        cout << "[1] Punctuation: " << (settings.includePunctuation ? GREEN "ON" : RED "OFF") << RESET << endl;
        cout << "[2] Numbers: " << (settings.includeNumbers ? GREEN "ON" : RED "OFF") << RESET << endl;
        cout << "[3] Back to Menu" << endl;
        cout << endl;

        cout << GRAY << "Note: These settings only apply to WORDS mode" << RESET << endl;
        cout << endl;

        cout << "Enter your choice: ";
    }

    void run(){
        string input;

        while(true){
            switch(currentState){
                case gameState::MENU: {
                    while(true){
                        showMenu();
                        getline(cin, input);
                        if(input == "1"){
                            currentState = gameState::TEST_OPTIONS;
                            break;
                        } else if(input == "2"){
                            currentState = gameState::SETTINGS;
                            break;
                        } else if(input == "3"){
                            cout << GREEN << "Thanks for playing. Goodbye!" << RESET << endl;
                            return;
                        } else {
                            cout << RED << "Please try again and enter an integer 1-3." << RESET << endl;
                        }
                    }
                }
                    break;

                case gameState::TEST_OPTIONS: {
                    while(true){
                        showTestOptions();
                        getline(cin, input);
                        if(input == "1" || input == "2" || input == "3" || input == "4"){
                            handleTestOptions(input);
                            break;
                        } else {
                            cout << RED << "Please try again and enter an integer 1-4." << RESET << endl;
                        }
                    }
                }
                    break;

                case gameState::ACTIVE_TEST: {
                    TermiosGuard tg;
                    tg.enableRaw();

                    // initial draw
                    cout << "\x1b[2J\x1b[H"; // clear and move cursor home
                    displayColorText();
                    cout << endl;

                    char c{};
                    while(currentState == gameState::ACTIVE_TEST){
                        ssize_t n = read(STDIN_FILENO, &c, 1);
                        if(n <= 0) continue;

                        // Ctrl-C
                        if(c == 3){
                            tg.restore();
                            return;
                        }

                        // backspace (127) or '\b' (8)
                        if(c == 127 || c == 8){
                            if(!userInput.empty()){
                                size_t idx = userInput.length() - 1;
                                // adjust stats
                                if(idx < targetText.length()){
                                    if(characterStatus[idx]) stats.correctChars--;
                                    else stats.incorrectChars--;
                                    characterStatus[idx] = false;
                                } else {
                                    // previously typed beyond target
                                    stats.incorrectChars = max(0, stats.incorrectChars - 1);
                                }
                                userInput.pop_back();
                                stats.totalChars = max(0, stats.totalChars - 1);
                            }
                        } else if(c == '\r' || c == '\n'){
                            // ignore enter during test
                        } else {
                            processCharacter(c);
                        }

                        updateTimer();

                        // redraw quickly
                        cout << "\x1b[2J\x1b[H"; // clear and move cursor home
                        displayColorText();
                        cout << endl;
                        cout << BOLD << "Time: " << RESET << elapsedTime << "s   ";
                        // update stats' view of current input so calculateStats can use it
                        stats.userInput = userInput;
                        stats.targetText = targetText;
                        stats.characterStatus = characterStatus;
                        stats.calculateStats(elapsedTime);
                        cout << BOLD << "WPM: " << RESET << stats.netWPM << "   ";
                        cout << BOLD << "Accuracy: " << RESET << stats.accuracy << "%" << endl;
                        cout << endl;
                        cout << "Typed: " << userInput << endl;
                        cout << flush;

                        // if finished, break to show results
                        if(currentState == gameState::RESULTS) break;
                    }

                    tg.restore();
                }
                    break;

                case gameState::RESULTS: {
                    while(true){
                        showResults();
                        getline(cin, input);
                        if(input == "1"){
                            startTest();
                            break;
                        } else if(input == "2"){
                            currentState = gameState::MENU;
                            break;
                        } else {
                            cout << RED << "Please try again and enter an integer 1-2." << RESET << endl;
                        }
                    }
                }
                    break;

                case gameState::SETTINGS: {
                    while(true){
                        showSettings();
                        getline(cin, input);

                        if(input == "1"){
                            settings.includePunctuation = !settings.includePunctuation;
                            // stay in settings to allow multiple changes
                        } else if(input == "2"){
                            settings.includeNumbers = !settings.includeNumbers;
                            // stay in settings
                        } else if(input == "3"){
                            currentState = gameState::MENU;
                            break;
                        } else {
                            cout << RED << "Please try again and enter an integer 1-3." << RESET << endl;
                        }
                    }
                }
                    break;
            }
        }
    }
};


int main(){
    cout << CYAN << "Initializing Typing Speed Test..." << RESET << endl;
    cout << endl;

    // init game
    typingGame game;

    if(!game.init()){
        cerr << RED << "ERROR: Failed to initialize game" << RESET << endl;
        return -1;
    }

    cout << endl;
    cout << GREEN << "Game ready! Starting..." << RESET << endl;
    cout << endl;

    // run game loop
    game.run();

    return 0;
}