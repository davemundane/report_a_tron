var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext("2d");

var rightPressed = false;
var leftPressed = false;
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
document.addEventListener("mousemove", mouseMoveHandler, false);

class TheBall {
  constructor() {
    this.x = canvas.width/2;
    this.y = canvas.height-30;
    this.ballRadius = 10;
    var directionPicker = Math.floor(Math.random() * 2)
    if (directionPicker == 1) {
      this.dx = 2.4;
      this.dy = -2.4;
    }
    else {
      this.dx = -2.4;
      this.dy = 2.4;
    }
    this.trailLength = 25;
    this.positions = []
  }

  drawBall(value) {

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.ballRadius, 0, Math.PI*2);
      ctx.fillStyle = "#17b0a8";
      ctx.fill();
      ctx.closePath();

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.ballRadius - 3, 0, Math.PI*2);
      ctx.fillStyle = "#1d2121";
      ctx.fill();
      ctx.closePath();

      ctx.beginPath();
      ctx.arc(this.x, this.y, this.ballRadius - 8, 0, Math.PI*2);
      ctx.fillStyle = "#17b0a8";
      ctx.fill();
      ctx.closePath();
      this.storeLastPosition();
      this.drawTrail();
  }

  storeLastPosition() {
    this.positions.push({ x: this.x, y: this.y });
    if (this.positions.length > this.trailLength) {
      this.positions.shift();
    }
  }

  drawTrail() {
    for(var i=0; i < this.positions.length; i++) {
      var ratio = (i + 1) / this.positions.length;
      ctx.globalAlpha = 0.5;
      ctx.beginPath();
      ctx.arc(this.positions[i].x, this.positions[i].y, this.ballRadius, 0, Math.PI*2);
      ctx.fillStyle = "rgba(109, 232, 223, " + ratio / 2 + ")";
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.closePath();
    }
  }

  updatePosition() {
    this.x += this.dx;
    this.y += this.dy;
  }

  bounce() {
    if (this.x + this.dx < this.ballRadius || this.x + this.dx > canvas.width - this.ballRadius) {
      this.dx = -this.dx;
    }

    if (this.y + this.dy < this.ballRadius) {
      this.dy = -this.dy;
    }
    else if (this.y + this.dy > canvas.height - this.ballRadius) {
      if (this.x > paddle.paddleX && this.x < paddle.paddleX + paddle.paddleWidth) {
        this.dy = -this.dy;
        this.dx = this.dx * 1.08;
        this.dy = this.dy * 1.08;
      }
      else {
        var mytext = document.getElementById("writing")
        mytext.innerHTML = "GAME OVER";
        document.location.reload();
      }
    }
  }

  reflectBall() {
    this.dy = -this.dy
  }
}

class ThePaddle {
  constructor() {
    this.paddleHeight = 10;
    this.paddleWidth = 75;
    this.paddleX = (canvas.width - this.paddleWidth) / 2;

  }

  drawPaddle() {

    ctx.save();
    ctx.beginPath();
    ctx.rect(this.paddleX, canvas.height - this.paddleHeight, this.paddleWidth, this.paddleHeight);
    ctx.shadowColor = "#f5626c"
    ctx.shadowBlur = 10;
    ctx.fillStyle = "#b30b16";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.rect(this.paddleX + 2, canvas.height - this.paddleHeight + 2, this.paddleWidth - 4, this.paddleHeight - 4);
    ctx.fillStyle = "#131414";
    ctx.fill();
    ctx.closePath();

    ctx.restore();
  }

  updatePaddle() {
    if(rightPressed) {
      this.paddleX += 7;
      if (this.paddleX + this.paddleWidth > canvas.width) {
        this.paddleX = canvas.width - this.paddleWidth;
      }
    }
    else if(leftPressed) {
      this.paddleX -= 7;
      if (this.paddleX < 0) {
        this.paddleX = 0;
      }
    }
  }
}

class TheBricks {
  constructor() {
    this.brickRowCount = 3;
    this.brickColumnCount = 9;
    this.brickWidth = 75;
    this.brickHeight = 20;
    this.brickPadding = 5;
    this.brickOffsetTop = 30;
    this.brickOffsetLeft = 40;
    this.bricks = []
    this.hexCodes = ["#9c3376","#9c339c", "#58339c", "#33469c", "#33809c", "#339c6f", "#569c33", "#9c9733", "#9c4d33"]
  }

  createBricks() {
    for(var c=0; c<this.brickColumnCount; c++) {
      this.bricks[c] = [];
      for(var r=0; r<this.brickRowCount; r++) {
        var hexColour = this.hexCodes[Math.floor(Math.random() * this.hexCodes.length)]
        this.bricks[c][r] = { x: 0, y: 0, colour: hexColour, status: 1 };
      }
    }
  }

  drawBricks() {
    ctx.save();
    for(var c=0; c<this.brickColumnCount; c++) {
      for(var r=0; r<this.brickRowCount; r++) {
        if (this.bricks[c][r].status == 1) {
          var brickX = (c*(this.brickWidth + this.brickPadding)) + this.brickOffsetLeft;
          var brickY = (r*(this.brickHeight + this.brickPadding)) + this.brickOffsetTop;

          this.bricks[c][r].x = brickX;
          this.bricks[c][r].y = brickY;
          ctx.beginPath();
          ctx.rect(brickX, brickY, this.brickWidth, this.brickHeight);
          ctx.fillStyle = this.bricks[c][r].colour;
          ctx.shadowColor = "#4d4d4d"
          ctx.shadowBlur = 10;
          ctx.fill();
          ctx.closePath();
        }
      }
    }
    ctx.restore();
  }

  removeBrick(c,r) {
    this.bricks[c][r].status = 0;
  }
}

class TheScore {
  constructor() {
    this.score = 0;
  }

  incrementScore(value) {
    this.score += value;
  }

  drawScore() {
    ctx.font = "16px Arial";
    ctx.fillStyle = "#38d3e8";
    ctx.fillText("Score: "+this.score, 8, 20);
  }
}

let ball = new TheBall();
let paddle = new ThePaddle();
let bricks = new TheBricks();
let score = new TheScore();
var value = 0;

bricks.createBricks();

function draw() {
  value += 1;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ball.drawBall(value);
  ball.updatePosition();
  ball.bounce();

  paddle.drawPaddle();
  paddle.updatePaddle();

  bricks.drawBricks();

  score.drawScore();

  collisionDetection(ball.x,ball.y)

  requestAnimationFrame(draw);


}

function collisionDetection(ballX, ballY) {
    for(var c=0; c<bricks.brickColumnCount; c++) {
        for(var r=0; r<bricks.brickRowCount; r++) {
            var b = bricks.bricks[c][r];
            if (bricks.bricks[c][r].status == 1) {
              if(ballX > b.x && ballX < b.x+bricks.brickWidth && ballY > b.y && ballY < b.y+bricks.brickHeight) {
                  ball.reflectBall();
                  bricks.removeBrick(c,r);
                  score.incrementScore(1);
                  if (score.score == bricks.brickRowCount * bricks.brickColumnCount) {
                    alert("YOU WIN");
                    document.location.reload();
                  }
                }
            }
        }
    }
}

function mouseMoveHandler(e) {
    var relativeX = e.clientX - canvas.offsetLeft;
    if(relativeX > 0 && relativeX < canvas.width) {
        paddle.paddleX = relativeX - paddle.paddleWidth/2;
    }
}

function keyDownHandler(e) {
    if(e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = true;
    }
    else if(e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if(e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = false;
    }
    else if(e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = false;
    }
}

draw();
