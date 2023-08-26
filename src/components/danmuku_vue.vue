<template>
  <div class="danmu-container" ref="danmuContainer">
    <div
      class="danmu"
      v-for="(danmu, index) in danmus"
      :key="index"
      :style="{ top: `${index * 11.5}%`, backgroundColor: danmu.color === '#527CE7' ? 'transparent' : danmu.color }"
    >
      <div class="color-block"></div>
      {{ danmu.content }}
    </div>
  </div>
  <div v-if="colorPickerVisible" class="color-picker">
      <button v-for="(color, index) in colors"
              :key="index"
              :style="{ backgroundColor: color }"
              @click="selectedColor = color; colorPickerVisible = false;"
      ></button>
  </div>
  <div style="position: relative; top: 103.5% ; left: 5%; height: 10%;">
    <button @click="colorPickerVisible = !colorPickerVisible" 
            @blur="colorPickerVisible = false"
            :style="{ backgroundColor: selectedColor }"
            style="position: absolute; left: 1px; top:1px; border: none; padding:  0; height: 60%; aspect-ratio: 1 / 1;"
    ></button>
  </div>
  <div style="position: relative; top: 101%; left: 12%; width: 69%; height: 8%;">
    <input style="position: relative; border: none; width: 100%; height: 100%;" @mousedown.stop="" @keyup.enter="send" type="text" v-model="message"/>
    <button @click="send" style="position: absolute; top: 10%; left: 103%; aspect-ratio: 1 / 1; height: 100%; border: none; background: none; padding: 0;">
      <img id='send_button' src="../assets/button/danmuku_send.png" alt="Live Background" style="position: relative; height: 90%;">
    </button>
  </div>
<audio id="haisin_superchat" src="require('../assets/sound/haisin_superchat.wav')" type="audio/mpeg" style="display: none;"></audio>
</template>

<script>
import { debounce } from 'lodash';
export default {
  data() {
    return {
      message: '',
      danmus: [],
      maxDanmuCount: 20, // 最多显示20条弹幕
      timer: null,
      socket: null,
      colors: ['#527CE7', '#A2B6EA', '#8AD4FA', '#8CFCc7', '#FBFE92', '#FDC915', '#EA9FE5', '#E75352'], // 颜色列表
      selectedColor: '#527CE7', // 默认颜色为蓝色（无背景）
      colorPickerVisible: false, // 控制颜色选择器的显示和隐藏
      sound: null,
    };
  },
  methods: {
    playSound() {
      let sound = new Audio(require('../assets/sound/haisin_superchat.wav'));
      sound.play();
    },
    send() {
      //if (this.message.trim() !== '') {
        const danmu = { content: this.message, color: this.selectedColor };
        this.addDanmu(danmu);
        // 向 WebSocket 服务器发送消息
        this.socket.send(JSON.stringify(danmu));
        this.message = '';
      //}
    },
    addDanmu(danmu) {
      if (this.danmus.length >= this.maxDanmuCount) {
        this.danmus.shift(); // 删除最早的弹幕
      }
      if(danmu.color != '#527CE7'){
        this.playSound();
      }
      this.danmus.push(danmu); // 将新弹幕插入到尾部处
      this.$nextTick(() => {
        const container = this.$refs.danmuContainer;
        const isAtBottom = container.scrollTop + container.clientHeight + 60 >= container.scrollHeight;
        if (isAtBottom) {
          container.scrollTop = container.scrollHeight;
        }
      });
    }
  },
  mounted() {
    this.socket = new WebSocket('wss://sicktock.com:8765');
    this.sound = new Audio(require('../assets/sound/haisin_superchat.wav'));
    this.socket.onopen = () => {
      console.log('Connected to the websocket server.');
    };

    this.socket.onmessage = (event) => {
      console.log('Received: ' + event.data);
      const danmu = JSON.parse(event.data);
      this.addDanmu(danmu);
    };

    this.socket.onclose = () => {
      console.log('Disconnected from the websocket server.');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error: ', error);
    };

    // 用debounce函数来检测用户何时停止滚动
    const onScroll = debounce(() => {
      this.isUserScrolling = false;
    }, 1000);

    // 添加滚动事件监听器
    this.$refs.danmuContainer.addEventListener('scroll', () => {
      this.isUserScrolling = true;
      onScroll();
    });
  },
  beforeUnmount() {
    clearInterval(this.timer);
    if (this.socket) {
      this.socket.close();
    }
  },
};
</script>

<style>
  .danmu-container {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    border: 0px;
  }
  @font-face {
    font-family: 'MyCustomFont';
    src: url('../assets/fonts/zpix.ttf') format('truetype'),
        url('../assets/fonts/PixelMplus10-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
  }
  .danmu {
    position: absolute;
    width: 95%;
    left: 5%;
    height: 11.5%; /*superchat背景高度*/
    line-height: 100%; /*弹幕字体高度*/
    padding-left: 10%;
    box-sizing: border-box;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: 'MyCustomFont', sans-serif;
    font-size: 1.5vi;
    color:#4D23CF
  }
  .color-block {
    position: absolute;
    left: 3%;
    top: 25%;
    aspect-ratio: 1 / 1; /* 宽度和高度的比例是1:1，形成一个正方形 */
    height: 35%;
    background-color: #527CE7;
  }
  .color-picker {
    position: absolute;
    top: 80%;
    left: 5%;
    display: flex;
    flex-wrap: wrap;
    width: 35%;
    padding: 5px;
    background: #fff;
    border: 1px solid #ccc;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
  }
  .color-picker button {
    width: 15%;
    aspect-ratio: 1 / 1; /* 宽度和高度的比例是1:1，形成一个正方形 */
    border: 0px;
    margin: 4px;
}

</style>
