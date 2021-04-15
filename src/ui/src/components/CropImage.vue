<template lang="html">
  <div class="wrapper">
    <VueCropper
      ref="cropper"
      class="wrapper-cropper"
      :src="image"
      dragMode="move"
      :minCropBoxWidth="280"
      :minCropBoxHeight="280"
      :minCanvasWidth="280"
      :minCanvasHeight="280"
      :minContainerWidth="280"

      :aspectRatio="1"
      :initialAspectRatio="1"
      :restore="true"
      :guides="false"
      :center="false"
      :highlight="false"

      :cropBoxMovable="false"
      :cropBoxResizable="false"
      :toggleDragModeOnDblclick="false"
      :viewMode='1'
      :autoCrop="true"
      :data="{
        width: 280,
        height: 280,
      }"
      alt="Source Image"
      :ready="onReady"
    />
    <button @click="cropImage" class="button-primary">Save</button>
    <button @click="$emit('close')" class="close-button">Cancel</button>
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';

function getRoundedCanvas(sourceCanvas) {
    let canvas = document.createElement('canvas');
    let context = canvas.getContext('2d');
    let width = sourceCanvas.width;
    let height = sourceCanvas.height;

    canvas.width = width;
    canvas.height = height;
    context.imageSmoothingEnabled = true;
    context.drawImage(sourceCanvas, 0, 0, width, height);
    context.globalCompositeOperation = 'destination-in';
    context.beginPath();
    context.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, 2 * Math.PI, true);
    context.fill();
    return canvas;
}

export default {
    name: 'CropImage',
    props: ['image'],
    data(){
      return {
        cropImg: ''
      }
    },
    methods: {
      cropImage() {
        const canvasCopped = this.$refs.cropper.getCroppedCanvas()

        this.cropImg = getRoundedCanvas(canvasCopped).toDataURL();
        this.$emit('change', this.cropImg)
        this.$emit('close')
      },
      onReady(){
        const imageData = this.$refs.cropper.getImageData()
        const cropData = this.$refs.cropper.getData(true)

        this.$refs.cropper.setData({
          y: (imageData.naturalHeight - cropData.height) / 2,
          x: (imageData.naturalWidth - cropData.width) / 2,
        })
      }
    },
    components: {
      VueCropper
    }
}
</script>

<style lang="less" scoped>
  /deep/ .cropper-bg {
    background-image: none;
    height: 280px;
  }

  /deep/ .button-primary {
    margin-top: 10px;
  }

  .wrapper {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    position: relative;
    padding-bottom: 20px;
  }

  /deep/ .cropper-view-box {
    border-radius: 50%;
  }
</style>
