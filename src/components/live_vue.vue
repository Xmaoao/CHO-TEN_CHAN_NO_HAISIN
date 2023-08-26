<template>
  <div style="position: relative;">
    <img id = 'live' src="../assets/live/live_bkg.png" alt="Live Background" style="height: 100%;"/>
    <div style="position: absolute; top: 0%; left: 0%; width: 100%; height: 100%;">
      <StreamComponents></StreamComponents>
    </div>
    <div style="position: absolute; top: 19%; left: 56%; width: 30.1%; height: 46.5%;">
      <DanmukuComponents></DanmukuComponents>
    </div>
  </div>
</template>

<script>
  import DanmukuComponents from "./danmuku_vue.vue"
  import StreamComponents from "./stream_vue.vue"
  export default{
    components:{
      StreamComponents,
      DanmukuComponents
    }
  }
</script>

