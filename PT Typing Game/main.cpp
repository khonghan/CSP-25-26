#include "include.cpp"

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

    std::string userInput;
    std::string targetText;
    std::vector<bool> characterStatus; // track (in)correct characters

    void calculateStats(double elapsedTime){
        timeTaken = elapsedTime;

        // Recompute totals from the provided userInput/characterStatus so backspaces are reflected immediately
        int computedTotal = static_cast<int>(userInput.length());
        int computedCorrect = 0;
        for(int i = 0; i < computedTotal; ++i){
            if(i < static_cast<int>(characterStatus.size()) && characterStatus[i]) computedCorrect++;
        }
        int computedIncorrect = std::max(0, computedTotal - computedCorrect);

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
    int wordCount = 15;
    int timeLimit = 30; // seconds for time mode
    std::string customText = "";
    bool includePunctuation = false;
    bool includeNumbers = false;
};

class textGenerator {
private:
    std::vector<std::string> wordList;

public:
    textGenerator(){
        srand(static_cast<unsigned int>(time(0)));
    }

    // load words from file into wordList
    bool generateWordList(const std::string& filename){
        std::ifstream file(filename);
        if(!file.is_open()){
            std::cerr << RED << "Error opening word list file: " << filename << RESET << std::endl;
            return false;
        }

        std::string word;
        wordList.clear();

        while(file >> word){
            // filter out non-alphabetic words
            if(std::all_of(word.begin(), word.end(), ::isalpha)){
                std::transform(word.begin(), word.end(), word.begin(), ::tolower);
                wordList.push_back(word);
            }
        }

        file.close();

        if(wordList.empty()){
            std::cerr << RED << "Error: Word list is empty/invalid." << RESET << std::endl;
            return false;
        }

        std::cout << GREEN << "Loaded " << wordList.size() << " words successfully!" << RESET << std::endl;
        return true;
    }

    std::string getRandomWord(){
        if(wordList.empty()) return "error";
        return wordList[rand() % wordList.size()];
    }

    std::string generateText(int wordCount, const gameSettings& settings){
        /* first version of generating text
        std::string generatedText;
        for(int i = 0; i < wordCount; i++){
            generatedText += getRandomWord();
            if(i < wordCount - 1){
                generatedText += " ";
            }
        }

        return generatedText;
        */

        std::string result;
        
        // iterate a specified # of words
        for(int i = 0; i < wordCount; i++){
            std::string word = getRandomWord();

            // add numbers if enabled in settings
            if(settings.includeNumbers && (rand() % 5 ==0)){
                word += std::to_string(rand() % 100);
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

    std::string targetText;
    std::string userInput;
    std::vector<bool> characterStatus; // track (in)correct characters

    std::chrono::steady_clock::time_point testStartTime;
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
            std::cerr << RED << "Failed to load word list!" << RESET << std::endl;
            std::cerr << "Please ensure '1000-most-common-words.txt' file exists in the same directory." << std::endl;
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
        std::cout << CYAN << BOLD;
        std::cout << "╔════════════════════════════════════════════════════════════╗" << std::endl;
        std::cout << "║                   SUPER COOL TYPING TEST                   ║" << std::endl;
        std::cout << "╚════════════════════════════════════════════════════════════╝" << RESET << std::endl;
        std::cout << std::endl;
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
                    int wordEstimate = std::max(30, settings.timeLimit * 2);
                    targetText = textGen.generateText(wordEstimate, settings);
                }
                break;

            case testType::CUSTOM:
                targetText = settings.customText;
                if(targetText.empty()){
                    std::cout << RED << "No custom text. Returning to menu..." << RESET << std::endl;
                    std::cin.get();
                    currentState = gameState::MENU;
                    return;
                }
                break;
        }

        characterStatus.clear();
        characterStatus.resize(targetText.length(), false);

        currentState = gameState::ACTIVE_TEST;

        std::cout << YELLOW << "Test starting with " << targetText.length() << " characters..." << RESET << std::endl;
        std::cout << std::endl;
    }

    // process typed character
    void processCharacter(char c){
        // start timer when user first inputs
        if(!testStarted){
            testStarted = true;
            testStartTime = std::chrono::steady_clock::now();
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
            auto now = std::chrono::steady_clock::now();
            elapsedTime = std::chrono::duration<double>(now - testStartTime).count();

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
                    std::cout << GREEN << targetText[i] << RESET; // correct character
                } else {
                    std::cout << RED << targetText[i] << RESET; // incorrect character
                }
            } else if(i == userInput.length()){
                // current character
                std::cout << YELLOW << BOLD << targetText[i] << RESET;
            } else {
                std::cout << GRAY << targetText[i] << RESET;
            }
        }
        std::cout << std::endl;
    }

    void showMenu(){
        clearScreen();
        printHeader();

        std::cout << "Welcome! Test your typing speed and accuracy." << std::endl;
        std::cout << std::endl;

        std::cout << BOLD << "MENU OPTIONS:" << RESET << std::endl;
        std::cout << " [1] Test Options" << std::endl;
        std::cout << " [2] Settings" << std::endl;
        std::cout << " [3] Exit" << std::endl;
        std::cout << std::endl;

        std::cout << CYAN << "Current Mode: ";
        switch(settings.testMode){
            case testType::WORDS:
                std::cout << settings.wordCount << " words";
                break;
            case testType::TIME:
                std::cout << settings.timeLimit << " seconds";
                break;
            case testType::CUSTOM:
                std::cout << "Custom Text";
                break;
        }

        std::cout << RESET << std::endl;
        std::cout << std::endl;

        std::cout << "Enter your choice: ";
    }

    void showTestOptions(){
        clearScreen();

        std::cout << BOLD << "╔════════════════════════════════════════════════════════════╗" << std::endl;
        std::cout << "║                      TEST OPTIONS                          ║" << std::endl;
        std::cout << "╚════════════════════════════════════════════════════════════╝" << RESET << std::endl;
        std::cout << std::endl;

        std::cout << CYAN << "Choose your test type:" << RESET << std::endl;
        std::cout << std::endl;

        // test type WORDS
        std::cout << BOLD << "[1] Words Mode" << RESET << std::endl;
        std::cout << std::endl;

        // test type TIME
        std::cout << BOLD << "[2] Time Mode" << RESET << std::endl;
        std::cout << std::endl;

        // test type CUSTOM
        std::cout << BOLD << "[3] Custom Mode" << RESET << std::endl;
        std::cout << std::endl;

        std::cout << "[4] Return to Menu" << std::endl;
        std::cout << std::endl;

        std::cout << "Enter your choice (1-4): ";
    }

    void handleTestOptions(const std::string& choice){
        if(choice == "1"){ // WORDS
            clearScreen();
            // printHeader();

            std::cout << BOLD << "WORDS MODE" << RESET << std::endl;
            std::cout << std::endl;
            std::cout << "  [a] 10 words" << std::endl;
            std::cout << "  [b] 25 words" << std::endl;
            std::cout << "  [c] 50 words" << std::endl;
            std::cout << "  [d] 100 words" << std::endl;
            std::cout << "  [e] Custom word count" << std::endl;
            std::cout << std::endl;
            std::cout << "Choice: ";

            std::string subchoice;
            std::getline(std::cin, subchoice);

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
                    std::cout << "Enter custom word count (1-500): ";
                    std::string line;
                    std::getline(std::cin, line);

                    if(line.empty()){
                        // if the user just pressed enter, prompt again
                        continue;
                    }

                    std::stringstream ss(line);
                    if(!(ss >> custom) || !(ss.eof())){
                        std::cout << RED << "Invalid input. Please enter a valid integer." << RESET << std::endl;
                        continue;
                    }

                    if(custom > 0 && custom <= 500){
                        settings.wordCount = custom;
                        break;
                    } else {
                        std::cout << RED << "Please enter an integer between 1 and 500." << RESET << std::endl;
                    }
                }
            }

            // if subchoice wasn't recognized, inform user and return to options
            if(subchoice != "a" && subchoice != "b" && subchoice != "c" && subchoice != "d" && subchoice != "e"){
                std::cout << RED << "Invalid choice. Valid: a, b, c, d, e. Press Enter to continue..." << RESET << std::endl;
                std::cin.get();
                currentState = gameState::TEST_OPTIONS;
                return;
            }

            std::cout << GREEN << "Set to " << settings.wordCount << " words mode!" << RESET << std::endl;
            std::cout << "Press Enter to start test...";
            std::cin.get();
            startTest();

        } else if(choice == "2"){
            clearScreen();
            // printHeader();

            std::cout << BOLD << "TIME MODE" << RESET << std::endl;
            std::cout << std::endl;
            std::cout << "  [a] 15 seconds" << std::endl;
            std::cout << "  [b] 30 seconds" << std::endl;
            std::cout << "  [c] 60 seconds" << std::endl;
            std::cout << "  [d] 120 seconds" << std::endl;

            std::string subchoice;
            std::getline(std::cin, subchoice);

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
                std::cout << RED << "Invalid choice. Valid: a, b, c, d. Press Enter to continue..." << RESET << std::endl;
                std::cin.get();
                currentState = gameState::TEST_OPTIONS;
                return;
            }

            std::cout << GREEN << "Set to " << settings.timeLimit << " seconds mode!" << RESET << std::endl;
            std::cout << "Press Enter to start test...";
            std::cin.get();
            startTest();

        } else if(choice == "3"){
            clearScreen();
            // printHeader();

            std::cout << BOLD << "CUSTOM MODE" << RESET << std::endl;
            std::cout << std::endl;
            std::cout << "Enter your custom text (press Enter when done):" << std::endl;
            std::cout << CYAN << "> " << RESET;

            settings.testMode = testType::CUSTOM;

            while(true){
                std::getline(std::cin, settings.customText);
                if(settings.customText.empty()){
                    std::cerr << RED << "Custom text is empty. Please enter something for custom text." << RESET << std::endl;
                    std::cout << CYAN << "> " << RESET;
                    continue;
                }
                break;
            }

            std::cout << GREEN << "Custom text set!" << RESET << std::endl;
            std::cout << "Press Enter to start test...";
            std::cin.get();
            startTest();

        } else if(choice == "4"){
            currentState = gameState::MENU;
        } else {
            std::cout << RED << "Invalid option. Please select an integer 1-4. Press Enter to continue..." << RESET << std::endl;
            std::cin.get();
            currentState = gameState::TEST_OPTIONS;
        }
    }

    void showTest(){
        clearScreen();
        // printHeader();

        updateTimer();

        std::cout << BOLD;
        if(settings.testMode == testType::TIME){
            double timeRemaining = settings.timeLimit - elapsedTime;
            if(timeRemaining < 0) timeRemaining = 0;
            std::cout << "TIME REMAINING: " << std::fixed << std::setprecision(1)
                      << timeRemaining << "s / " << settings.timeLimit << "s" << RESET << std::endl;
        } else {
            std::cout << "TIME: " << std::fixed << std::setprecision(1)
                      << elapsedTime << "s" << RESET << std::endl;
        }

        std::cout << "Progress: " << userInput.length() << " / " << targetText.length() << " characters (" 
                  << (int)((float)userInput.length() / targetText.length() * 100) << "%)" << std::endl;

        std::cout << "Correct: " << GREEN << stats.correctChars << RESET
                  << " | Incorrect: " << RED << stats.incorrectChars << RESET << std::endl;
        
        std::cout << std::endl;

        std::cout << "─────────────────────────────────────────────────────────" << std::endl;
        std::cout << BOLD << "TYPE THIS:" << RESET << std::endl;
        std::cout << std::endl;

        displayColorText();

        std::cout << std::endl;
        std::cout << "─────────────────────────────────────────────────────────" << std::endl;
        std::cout << std::endl;

        std::cout << BOLD << "YOUR INPUT:" RESET << std::endl;
        std::cout << userInput << std::endl;
        std::cout << std::endl;

        std::cout << GRAY << "(Type the text above. Press ESC to cancel)" << RESET << std::endl;
    }

    void showResults(){
        clearScreen();

        std::cout << GREEN << BOLD << "╔════════════════════════════════════════════════════════════╗" << std::endl;
        std::cout << "║                     TEST COMPLETE!                         ║" << std::endl;
        std::cout << "╚════════════════════════════════════════════════════════════╝" << RESET << std::endl;
        std::cout << std::endl;

        std::cout << CYAN << BOLD << "PERFORMANCE SUMMARY:" << RESET << std::endl;
        std::cout << "─────────────────────────────────────────────────────────" << std::endl;
        std::cout << std::endl;

        std::cout << "Time Taken: " YELLOW << std::fixed << std::setprecision(2)
                  << stats.timeTaken << " seconds" << RESET << std::endl;
        std::cout << std::endl;

        std::cout << BOLD << "Speed:" << RESET << std::endl;
        std::cout << " Raw WPM: " << MAGENTA << std::fixed << std::setprecision(1)
                  << stats.rawWPM << RESET << std::endl;
        std::cout << " Net WPM: " << MAGENTA << BOLD << stats.netWPM << RESET << std::endl;
        std::cout << std::endl;

        std::cout << BOLD << "Accuracy:" << RESET << std::endl;
        std::cout << " Overall: ";
        if(stats.accuracy >=90) std::cout << GREEN;
        else if(stats.accuracy >= 80) std::cout << YELLOW;
        else std::cout << RED;
        std::cout << BOLD << stats.accuracy << "%" << RESET << std::endl;
        std::cout << std::endl;

        std::cout << BOLD << "Character Stats:" << RESET << std::endl;
        std::cout << " Total: " << stats.totalChars << std::endl;
        std::cout << "  Correct: " << GREEN << stats.correctChars << RESET << std::endl;
        std::cout << "  Incorrect: " << RED << stats.incorrectChars << RESET << std::endl;
        std::cout << std::endl;

        std::cout << "─────────────────────────────────────────────────────────" << std::endl;
        std::cout << std::endl;

        std::cout << "Press [1] to try again, [2] for menu: ";
    }

    void showSettings(){
        clearScreen();
        // printHeader();

        std::cout << BOLD << "GENERAL SETTINGS" << RESET << std::endl;
        std::cout << "─────────────────────────────────────────────────────────" << std::endl;
        std::cout << std::endl;

        std::cout << "[1] Punctuation: " << (settings.includePunctuation ? GREEN "ON" : RED "OFF") << RESET << std::endl;
        std::cout << "[2] Numbers: " << (settings.includeNumbers ? GREEN "ON" : RED "OFF") << RESET << std::endl;
        std::cout << "[3] Back to Menu" << std::endl;
        std::cout << std::endl;

        std::cout << GRAY << "Note: These settings only apply to WORDS mode" << RESET << std::endl;
        std::cout << std::endl;

        std::cout << "Enter your choice: ";
    }

    void run(){
        std::string input;

        while(true){
            switch(currentState){
                case gameState::MENU: {
                    while(true){
                        showMenu();
                        std::getline(std::cin, input);
                        if(input == "1"){
                            currentState = gameState::TEST_OPTIONS;
                            break;
                        } else if(input == "2"){
                            currentState = gameState::SETTINGS;
                            break;
                        } else if(input == "3"){
                            std::cout << GREEN << "Thanks for playing. Goodbye!" << RESET << std::endl;
                            return;
                        } else {
                            std::cout << RED << "Please try again and enter an integer 1-3." << RESET << std::endl;
                        }
                    }
                }
                    break;

                case gameState::TEST_OPTIONS: {
                    while(true){
                        showTestOptions();
                        std::getline(std::cin, input);
                        if(input == "1" || input == "2" || input == "3" || input == "4"){
                            handleTestOptions(input);
                            break;
                        } else {
                            std::cout << RED << "Please try again and enter an integer 1-4." << RESET << std::endl;
                        }
                    }
                }
                    break;

                case gameState::ACTIVE_TEST: {
                    TermiosGuard tg;
                    tg.enableRaw();

                    // initial draw
                    std::cout << "\x1b[2J\x1b[H"; // clear and move cursor home
                    displayColorText();
                    std::cout << std::endl;

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
                                    stats.incorrectChars = std::max(0, stats.incorrectChars - 1);
                                }
                                userInput.pop_back();
                                stats.totalChars = std::max(0, stats.totalChars - 1);
                            }
                        } else if(c == '\r' || c == '\n'){
                            // ignore enter during test
                        } else {
                            processCharacter(c);
                        }

                        updateTimer();

                        // redraw quickly
                        std::cout << "\x1b[2J\x1b[H"; // clear and move cursor home
                        displayColorText();
                        std::cout << std::endl;
                        std::cout << BOLD << "Time: " << RESET << elapsedTime << "s   ";
                        // update stats' view of current input so calculateStats can use it
                        stats.userInput = userInput;
                        stats.targetText = targetText;
                        stats.characterStatus = characterStatus;
                        stats.calculateStats(elapsedTime);
                        std::cout << BOLD << "WPM: " << RESET << stats.netWPM << "   ";
                        std::cout << BOLD << "Accuracy: " << RESET << stats.accuracy << "%" << std::endl;
                        std::cout << std::endl;
                        std::cout << "Typed: " << userInput << std::endl;
                        std::cout << std::flush;

                        // if finished, break to show results
                        if(currentState == gameState::RESULTS) break;
                    }

                    tg.restore();
                }
                    break;

                case gameState::RESULTS: {
                    while(true){
                        showResults();
                        std::getline(std::cin, input);
                        if(input == "1"){
                            startTest();
                            break;
                        } else if(input == "2"){
                            currentState = gameState::MENU;
                            break;
                        } else {
                            std::cout << RED << "Please try again and enter an integer 1-2." << RESET << std::endl;
                        }
                    }
                }
                    break;

                case gameState::SETTINGS: {
                    while(true){
                        showSettings();
                        std::getline(std::cin, input);

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
                            std::cout << RED << "Please try again and enter an integer 1-3." << RESET << std::endl;
                        }
                    }
                }
                    break;
            }
        }
    }
};


int main(){
    std::cout << CYAN << "Initializing Typing Speed Test..." << RESET << std::endl;
    std::cout << std::endl;

    // init game
    typingGame game;

    if(!game.init()){
        std::cerr << RED << "ERROR: Failed to initialize game" << RESET << std::endl;
        return -1;
    }

    std::cout << std::endl;
    std::cout << GREEN << "Game ready! Starting..." << RESET << std::endl;
    std::cout << std::endl;

    // run game loop
    game.run();

    return 0;
}