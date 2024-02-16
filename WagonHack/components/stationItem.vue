<template>
  <div class="wrapper">
    <div class="wagon-container" @click="onClick">
      <div class="flex w-[90%]">
        <img src="@/assets/images/station.svg" class="mr-4"/>
        <span class="font-bold truncate">{{ name }}</span>
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

    <transition name="opacity-transform">
    <div class="w-full p-4" v-show="extended">
      <div class="grid grid-cols-3 w-2/3 justify-items-center gap-2 items-center">
        <div />
        <div class="font-semibold">свободно</div>
        <div class="font-semibold">занято</div>
        <div>
          <img src="@/assets/images/train.svg" width="35"/>
        </div>
        <div class="station-circle" style="background : #34E079; width: 50px; height : 50px">
          <span>{{ trains.length - busyTrains.length }}</span>
        </div>

        <div class="station-circle" style="background : #E04434; width: 50px; height : 50px">
          <span>{{ busyTrains.length }}</span>
        </div>

        <div>
          <img src="@/assets/images/wagon.svg" width="35"/>
        </div>
        <div class="station-circle" style="background : #34E079; width: 50px; height : 50px">
          <span>{{ wagons.length - busyWagons.length }}</span>
        </div>

        <div class="station-circle" style="background : #E04434; width: 50px; height : 50px">
          <span>{{ busyWagons.length }}</span>
        </div>

      </div>
    </div>
    </transition>
  </div>

</template>


<script>

export default {
  data() {
    return {
      extended: false,
      busyWagons: [],
      busyTrains: []
    }
  },
  props: ['id', 'name', 'trains', 'wagons', 'longitude', 'latitude', 'extended_prop'],
  mounted() {
    if (this.extended_prop) {
      this.extended = this.extended_prop
    }


    if (!this.trains) {
      return
    }

    this.busyTrains = this.trains.filter(item => item['end_station_id'] !== item['current_station_id'])
    this.busyWagons = this.wagons.filter(item => item['current_station_id'] !== item['target_station_id'])
  },
  methods: {
    async onClick() {
      this.extended = !this.extended
      if (this.extended) {
        await this.$emit('stationFocus', [this.latitude, this.longitude], this.name, this.trains, this.wagons);
      }
    },
  },
  watch: {
    async extended(value) {
      if (!value) {
        await this.$emit('closeTrainItem')
      }
    }
  }
}

</script>

<style scoped>

.wagon-container {
  @apply px-4 py-3 w-full bg-[#FEF4F4] mb-1 flex;
  @apply cursor-pointer items-center;
}

</style>
