
class BoggleGame {

      constructor(boardId, secs = 60) {

        this.secs = secs;
        this.showTimer();
    
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        this.timer = setInterval(this.timer.bind(this), 1000); // call the timer function for every 1 sec
    
        $("#word-form", this.board).on("submit", this.getWord.bind(this));
    }
  
    async getWord(e) {

        e.preventDefault();
        let $input_word = $("#word", this.board);
        let word = $input_word.val();
    
        $("#word").val('');

        if (!word) {
            return;
        }
        
        if (this.words.has(word)) {
            this.showMessage(`${word} already found`);
            return;
        }

        const response = await axios.get("/check-word", { params: { word : word} });

        if (response.data.result === "not-a-word") {
            this.showMessage(`${word} is not a valid English word`);
        } else if (response.data.result === "not-on-board") {
            this.showMessage(`${word} is not found on this board`);
        } else {
            this.score += word.length;
            this.showScore()
            this.words.add(word)
            this.showMessage(`Word Added: ${word}`);
            this.showWord(word)
        }
    }

    showScore() {
        $(".score", this.board).text(this.score);
    }
    showTimer() {
        $(".timer", this.board).text(this.secs);
    }
    showMessage(msg) {
        $(".msg", this.board).text(msg);
    }

    showWord(word) {
        $(".word-list",this.board).append($("<li>", { text: word }));
    }

    // this func is called every 1 sec to decrease the countdown by 1 sec
    async timer() {

        this.secs = this.secs - 1; 
        this.showTimer();  // call the showTimer to display the new secs
    
        // if the time left reaches to 0 secs then clear the timer and call the recordFinalScore() to show the final score
        if (this.secs === 0) {
          clearInterval(this.timer);  
          await this.recordFinalScore();
        }
      }

    async recordFinalScore() {

        $("#word-form", this.board).hide(); // hide the input form 

        // make a post request to /store-score route to update the no_plays and highscore if appropriate
        const response = await axios.post("/store-score", { score: this.score });
    
        if (response.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`);
        } else {
            this.showMessage(`Final score: ${this.score}`);
        }
    }
}

