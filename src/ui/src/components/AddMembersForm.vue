<template lang="html">
  <div class="">
    <ValidationObserver v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(onSubmit)">
        <div class="add-img-wrapper" v-show="!croppedImage">
          <ValidationProvider ref="avatarInput" name="avatar" rules="required" v-slot="{ errors, validate }">
            <label class="add-img">
              <input @change="onChangePictureInput($event) || validate($event)" ref="imageInput" style="display: none" type="file" accept="image/jpeg,image/png">
              <span class="add-img-text">Choose photo</span>
            </label>
            <p class="error-text">{{ errors[0] }}</p>
          </ValidationProvider>
        </div>
        <div v-if="croppedImage" class="preview-photo">
          <div @click="removePhoto" class="wrapper-image">
            <img :src="croppedImage" alt="">
          </div>
        </div>
        <label>
          <ValidationProvider name="First Name" rules="required|alpha_dash" v-slot="{ errors }">
            <input v-model="name" placeholder="Fname">
            <span class="error-text">{{ errors[0] }}</span>
          </ValidationProvider>
        </label>
        <label>
          <ValidationProvider name="Last Name" rules="required|alpha_dash" v-slot="{ errors }">
            <input v-model="surname" placeholder="Lname">
            <span class="error-text">{{ errors[0] }}</span>
          </ValidationProvider>
        </label>
        <label>From which to give an employee in a company:</label>
        <SelectDate @change="dateString => in_company_from = dateString"/>
        <button :disabled="creatingUser" type="submit" class="button-primary submit-button">
          <div v-if="creatingUser" class="lds-dual-ring"></div>
          <span v-else >Add employee</span>
        </button>
        <button @click="close" type="button" class="close-button">Cancel</button>
      </form>
    </ValidationObserver>
    <modal width='420' height="auto" name='crop-modal' @before-close="cropModalClose">
      <CropImage :image='image' @change="onCropped" @close="$modal.hide('crop-modal')"/>
    </modal>
  </div>
</template>

<script>
// import PictureInput from 'vue-picture-input'
import CropImage from './CropImage'
import SelectDate from './SelectDate'
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
import { required, image, alpha_dash } from 'vee-validate/dist/rules'

extend('required', {
  ...required,
  message: "This field is required"
});
extend('alpha_dash', {
  ...alpha_dash,
  message: "The field contains inadmissible characters"
});

extend('image', {
  ...image,
  message: "This item is required"
});
import { addUser } from '../services/members'


export default {
  name: "AddMemberForm",
  components: {
    ValidationProvider,
    ValidationObserver,
    CropImage,
    SelectDate
  },
  data(){
    return {
      croppedImage: '',
      creatingUser: false,
      image: null,
      name: '',
      surname: '',
      in_company_from: '',
    }
  },
  computed: {
    user() {
      return {
        first_name: this.name,
        last_name: this.surname,
        photography: this.croppedImage,
        in_company_from: this.in_company_from
      }
    }
  },
  methods: {
    async onSubmit(){
      this.creatingUser = true

      try {
        await addUser(this.user)
        this.$notify({ title: 'Saved', type: 'success' });
        this.$root.$emit('triggerUpdateList')
        this.close()
      } catch (e) {
        this.$notify({ title: 'Something went wrong', type: 'error' });
      }

      this.creatingUser = false
    },
    close(){
      this.$emit('close')
    },
    onCropped(croppedImage){
      this.croppedImage = croppedImage
      this.$modal.hide('crop-modal')
    },
    onChangePictureInput(event) {
      let reader  = new FileReader()
      let file = event.target.files[0]
      this.$refs.avatarInput.validate()

      reader.onloadend = () => {
        this.image = reader.result;
        this.$modal.show('crop-modal')
      }

      if (file) {
        reader.readAsDataURL(file);
      } else {
        this.image = null
      }
    },
    cropModalClose(){
      if (!this.croppedImage) {
        this.removePhoto()
      }
    },
    removePhoto(){
      this.croppedImage = ''
      this.image = null
      this.$refs.avatarInput.value = ''
      this.$refs.imageInput.value = ''
    }
  }
}
</script>

<style lang="less" scoped>
@import '../assets/style/config.less';

.add-img {
  width: 120px;
  height: 120px;
  background: #E9EEEE;
  display: block;
  border-radius: 50%;
  margin: 0 auto;
  background-repeat: no-repeat;
  background-position: center 20px;
  background-image: url(../assets/images/avatar-placeholder.svg);
}

.add-img-wrapper {
  width: 120px;
  height: 120px;
  position: relative;
  margin: 0 auto;
  font-size: 11px;
  line-height: 13px;
  color: @global-color;
  text-align: center;

  label {
    cursor: pointer;
  }
}

.preview-photo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;


  .wrapper-image {
    width: 120px;
    height: 120px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;

    img {
      width: 100%;
      height: 100%;
    }
  }

  button {
    margin-top: 15px;
    line-height: 24px;
    padding: 0 10px;
  }
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.submit-button {
  margin-top: 40px;
}

.add-img-text {
  position: absolute;
  bottom: 20px;
  left: 50%;
  width: 100%;
  transform: translateX(-50%);
}

label {
  margin-top: 30px;
}

label, input {
  display: block;
  width: 100%;
}
</style>
