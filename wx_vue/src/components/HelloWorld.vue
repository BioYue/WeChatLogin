<template>
  <div>
    <div class="top">
      <img class="wximg" src="../assets/wechat.png" />
      <h1>WeChat扫码登录</h1>
    </div>
    <div class="qrdiv">
      <div class="qrbox" v-loading="loading">
        <img v-show="!loading" class="qrimg" :src="qr_url" alt="" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HelloWorld',
  data() {
    return {
      qr_url: '',
      scene: '',
      loading: true,

    }
  },

  mounted() {
    this.getQrUrl()
  },
  methods: {
    getQrUrl() {
      axios.get('https://api.xxxx.pro/api/weChatLogin').then((res) => {
        console.log(res.data);
        this.qr_url = res.data.url
        this.scene = res.data.scene
        this.loading = false
      })
      this.tem_poll = setInterval(this.loginPoll, 1000)
    },

    loginPoll() {
      axios.get('https://api.xxxx.pro/api/verifyLogin?scene=' + this.scene).then((res) => {
        console.log(res.data);
        if (res.data == 'success') {
          clearInterval(this.tem_poll)
          this.$notify({
            title: '登录成功',
            type: 'success',
            duration: 0
          });
          return;
        }
      })
    }
  }
}
</script>

<style scoped>
.top {
  display: flex;
  justify-content: center;
  margin: 120px 0 10px 0;
}

.wximg {
  width: 72px;
  height: 72px;
  padding-right: 12px;
  padding-top: 6px;
}

.qrbox {
  width: 346px;
  height: 346px;
  margin-top: 15px;
  border: 1px solid #e2e2e2;
}

.qrimg {
  width: 346px;
  height: 346px;
  /* border: 1px solid #e2e2e2; */
}

.qrdiv {
  display: flex;
  justify-content: center;
}
</style>
