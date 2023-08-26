<template>
  <div id="app">
    <img src="./assets/live/bkg/bg_side_bar_night2.png" alt="Left Image" id="left-image" />
    <img src="./assets/live/bkg/bg_side_bar_night2.png" alt="Right Image" id="right-image" />
    <!-- 更多组件可以在这里添加 -->
  </div>
  <LiveVue
    ref="livevue"
    id="live-windose"
    @mousedown="dragInit"
    :style="{ left: `${x}px`, top: `${y}px`, position: 'absolute'}"
    />
</template>
  
<script>
  window.onload = function() {
      var img = document.getElementById('left-image');
      var windose = document.getElementById('live-windose');
      windose.style.height = (img.clientHeight * 0.85) + 'px'; // 设置 div 的高度为图片高度的 85%
  }
  import LiveVue from './components/live_vue.vue';

  export default {
    components: {
      LiveVue
    },
    data() {
      return {
        selected: null,
        x_pos: 0, y_pos: 0,
        x_elem: 0, y_elem: 0,
        x: parseFloat(window.getComputedStyle(document.getElementById('app')).getPropertyValue('width')) / 8 + 20 , y: 10,
      }
    },
    methods: {
        dragInit(e) {
        e.preventDefault();
        const livevueElement = this.$refs.livevue.$el;
        const rect = livevueElement.getBoundingClientRect();
        const relativeY = e.clientY - rect.top;

        if (relativeY < 50) {
          this.selected = livevueElement;
          this.x_elem = e.clientX - livevueElement.offsetLeft;
          this.y_elem = e.clientY - livevueElement.offsetTop;
          document.onmousemove = this.moveElem;
          document.onmouseup = this.destroy;
        }
      },
      moveElem(e) {
        this.x_pos = e.clientX;
        this.y_pos = e.clientY;
        let appElement = document.getElementById('app');
        let appcomputedStyle = window.getComputedStyle(appElement);
        let appheight = appcomputedStyle.getPropertyValue('height');
        let appheightValue = parseFloat(appheight);
        let appWidth = appcomputedStyle.getPropertyValue('width');
        let appWidthValue = parseFloat(appWidth);
        if (this.selected !== null) {
          if(this.x_pos - this.x_elem >= appWidthValue / 8 && this.x_pos - this.x_elem + this.selected.offsetWidth <= appWidthValue / 8 * 7)
            this.x = this.x_pos - this.x_elem;
          if(this.y_pos - this.y_elem >= 0 && this.y_pos - this.y_elem + this.selected.offsetHeight <= appheightValue - 40)
          this.y = this.y_pos - this.y_elem;
        }
      },
      destroy() {
        this.selected = null;
        document.onmousemove = null;
        document.onmouseup = null;
      },
    },
    beforeUnmount() {
      document.onmousemove = null;
      document.onmouseup = null;
    },
  }
</script>
  
<style scoped>
  #app {
    background-image: url("./assets/live/bkg/FHDbg.png");
    background-size: cover;
    position: relative;
    height: 100%; /* 这会确保你的 div 至少和屏幕一样高，这样背景图片就会覆盖整个屏幕 */
    margin: 0;
    border: 0;
  }
  #left-image {
    height: 100%;
    object-fit: cover; /* 保持图片比例并填充容器 */
    position: absolute;
    left: 0;
    z-index: 1;
  }
  #right-image {
    height: 100%; 
    object-fit: cover; /* 保持图片比例并填充容器 */
    position: absolute;
    right: 0;
    transform: scaleX(-1); /* 通过 scaleX(-1) 实现图片镜像 */
    z-index: 1;
  }
  
</style>