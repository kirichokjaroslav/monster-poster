<template lang="html">
  <div class="date-container">
    <CustomSelect v-model="selectedDay"   :options="availableDays"  />
    <CustomSelect v-model="selectedMonth" :options="availableMonths" />
    <CustomSelect v-model="selectedYear"  :options="availableYears" />
  </div>
</template>

<script>
import CustomSelect from './CustomSelect.vue'

const availableMonths = [{
  label: 'Jan',
  value: 0
}, {
  label: 'Feb',
  value: 1
}, {
  label: 'Mar',
  value: 2
}, {
  label: 'Apr',
  value: 3
}, {
  label: 'May',
  value: 4
}, {
  label: 'Jun',
  value: 5
}, {
  label: 'Jul',
  value: 6
}, {
  label: 'Aug',
  value: 7
}, {
  label: 'Sep',
  value: 8
}, {
  label: 'Oct',
  value: 9
}, {
  label: 'Nov',
  value: 10
}, {
  label: 'Dec',
  value: 11
}]

export default {
  name: 'SelectDate',
  data(){
    return {
      yearFrom: 2000,
      availableMonths,
      selectedDay: {
        label: new Date().getDate(),
        value: new Date().getDate()
      },
      selectedMonth: availableMonths[new Date().getUTCMonth()],
      selectedYear: {
        label: new Date().getFullYear(),
        value: new Date().getFullYear()
      }
    }
  },
  watch: {
      selectedDate: {
        handler(){
          let monthString = (this.selectedMonth.value + 1) + '' // + 1 because getUTCMonth begin from 0
          monthString = monthString.length < 2 ? `0${monthString}` : monthString

          let dayString = this.selectedDay.value + ''
          dayString = dayString.length < 2 ? `0${dayString}` : dayString

          this.$emit('change', `${dayString}.${monthString}.${this.selectedYear.value}`)
        },
        immediate: true
      },
      availableDays(){
        this.fixSelectedDay()
      }
  },
  computed: {
    selectedDate() {
        return new Date(this.selectedYear.value, this.selectedMonth.value, this.selectedDay.value)
    },
    availableDays() {
      const dayCount = new Date(this.selectedYear.value, this.selectedMonth.value + 1, 0).getDate();

      const days = []
      for (var i = 0; i < dayCount; i++) {
        days.push({ label: i + 1, value: i + 1 })
      }
      return days
    },
    availableYears(){
      const milliSecondsDiff = new Date().getTime() - new Date(this.yearFrom, 0, 1).getTime()  // from 2000
      const yearsCount = Math.floor(milliSecondsDiff / (365.25 * 24 * 60 * 60 * 1000))

      const years = []
      for (var i = 0; i <= yearsCount; i++) {
        years.push({ label: this.yearFrom + i, value: this.yearFrom + i })
      }
      return years
    }
  },
  methods: {
    fixSelectedDay(){
      const dayIsAvailable = this.availableDays.find(({ value }) => value === this.selectedDay.value)

      if(!dayIsAvailable) {
        this.selectedDay = this.availableDays[this.availableDays.length - 1]
      }
    },
  },
  components: {
    CustomSelect
  }
}
</script>

<style lang="less" scoped>

.date-container {
  display: flex;
  justify-content: center;
  margin-top: 34px;
  width: 100%;

  & > * {
    margin-right: 30px;

    &:last-child {
      margin-right: 0
    }
  }
}

</style>
