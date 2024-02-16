<template>
  <div class="wrapper">
    <div class="wagon-container" @click="extended = !extended">
      <div class="flex w-[90%]">
        <img src="@/assets/images/wagon.svg" class="wagon-icon"/>
        <span>Вагон <b>{{ id }}</b></span>
      </div>

      <img
        src="@/assets/images/cross.svg"
        v-show="extended"
        width="20"
      />

      <img
        src="@/assets/images/dropdown.svg"
        v-show="!extended"
        width="20"
      />
    </div>

    <div class="wagon-details-container" v-show="extended">
      <div v-for="station in stations" :key="station.id">
        <div class="flex items-center cursor-pointer">
          <div class="station-circle">
            <span style="position: relative; top: -3px" v-show="station.name === '...'">...</span>
          </div>
          <span
              :class="[station.name !== '...' ? 'station-point-name' : 'ml-2']"
              v-show="station.name !== '...'"
          >{{ station.name }}</span>
        </div>
        <div
          class="red-line"
          v-show="stations.indexOf(station) !== stations.length - 1"
        ></div>
      </div>
      </div>
  </div>

</template>


<script>

export default {
  data() {
    return {
      extended: false,
      stations: []
    }
  },
  props: ['id', 'trainId', 'to', 'current'],
  mounted() {
      this.stations = [this.current]
      if (this.current !== this.to) {
        this.stations.push({ name : '...' })
        this.stations.push(this.to);
      }
  },
  watch: {
    async extended (value) {
      if (!value) {
          await this.$emit('closeWagonItem');
          return
      }

      await this.$emit('openWagonItem', this.to, this.current, this.id);

    }
  }
}

</script>

<style scoped>

.wagon-container {
  @apply px-4 py-3 w-full bg-[#FEF4F4] mb-1 flex;
  @apply cursor-pointer items-center;
}

.wagon-icon {
  @apply mr-4
}

.wagon-details-container {
  @apply w-full p-4;
}

</style>
