<template>
  <div>
    <div v-if="currentDisplayLine">
      <img id="StreamBackground" src="../assets/live/bkg/bg_stream_gold.png">
      <img id="ChoTenChan" v-if="currentDisplayLine.emoji" :src="getEmojiUrl(currentDisplayLine.emoji, currentFrame)" @load="onImageLoad">
      <div id="Subtitle" v-if="displayText">{{ displayText }}</div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      txtContent: '',
      parsedTxt: [],
      currentLine: 0,
      currentFrame: 0,
      totalFrames: 0,
      displayText: '',
      typingSpeed: 50,  // ms per character
    };
  },
  mounted() {
    this.loadTxt();
  },
  computed: {
    currentDisplayLine() {
      return this.parsedTxt[this.currentLine];
    }
  },
  methods: {
    async loadTxt() {
      try {
        const response = await fetch('./chotest.txt');
        this.txtContent = await response.text();
        this.parsedTxt = this.parseTxt(this.txtContent);
        this.showLines();
      } catch (error) {
        console.error('Failed to load txt file:', error);
      }
    },
    parseTxt(txt) {
      const lines = txt.split('\n');
      return lines.map(line => {
        const match = line.match(/{(.+?)}/);
        return {
          emoji: match ? match[1] : null,
          text: line.replace(/{.+?}/, '').trim(),
        };
      });
    },
    showLines() {
      if (this.currentLine < this.parsedTxt.length) {
        this.loadEmojiFrames(this.parsedTxt[this.currentLine].emoji).then(frames => {
          this.totalFrames = frames;
          this.animateEmoji();
          this.typeTextEffect(this.parsedTxt[this.currentLine].text, () => {
            setTimeout(() => {
              this.currentLine++;
              this.showLines();
            }, 5000);
          });
        });
      }
    },
    typeTextEffect(text, callback) {
      let index = 0;
      this.displayText = '';  // Reset the displayed text
      const typeInterval = setInterval(() => {
        if (index < text.length) {
          this.displayText += text.charAt(index);
          index++;
        } else {
          clearInterval(typeInterval);
          if (callback) callback();
        }
      }, this.typingSpeed);
    },
    async loadEmojiFrames(emoji) {
      try {
        const response = await fetch(`./assets/Cho/stream_cho_${emoji}/number.txt`);
        const text = await response.text();
        return parseInt(text.trim(), 10);
      } catch (error) {
        console.error('Failed to load emoji frames:', error);
      }
    },
    getEmojiUrl(emoji, frame) {
      return `../assets/Cho/stream_cho_${emoji}/stream_cho_${emoji}_${frame.toString().padStart(3, '0')}.png`;
    },
    animateEmoji() {
      if (this.currentFrame < this.totalFrames) {
        setTimeout(() => {
          this.currentFrame++;
          this.animateEmoji();
        }, 300); // 这里是每帧动画的延迟，可以根据实际情况调整
      } else {
        this.currentFrame = 0;
      }
    },
    onImageLoad() {
      // 检测图片是否加载成功，然后决定是否继续动画或其他操作
    },
  }
};
</script>

<style scoped>
  #StreamBackground{
    width: 50%;
    position: absolute;
    top: 20%;
    left: 5%;
  }
  #ChoTenChan{
    width: 50%;
    position: absolute;
    top: 20%;
    left: 5%;
  }
  @font-face {
    font-family: 'MyCustomFont'; /* 为字体指定一个名字 */
    src: url('../assets/fonts/zpix.ttf'); /* 指向字体文件的路径 */
  }
  #Subtitle{
    position: absolute;
    max-width: 40%;
    transform: translate(-50%, -100%);
    font-family: 'MyCustomFont', sans-serif;
    color: white;
    font-size: 1.5vi;
    background-color: #4D23CFBB;/*BB是透明度在十六进制中的表示*/
    line-height: 130%;
    padding: 5px;
    top: 65%;
    left: 30%;
  }
</style>
