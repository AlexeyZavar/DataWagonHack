<template>
  <div class="wagon-route-container" ref="block">
    <div class="header">
      <img
          class="cross-icon"
          src="@/assets/images/crossWhite.svg"
          @click="opened = false"
          v-show="opened"
      />
      <img
          class="cross-icon"
          src="@/assets/images/dropdownWhite.svg"
          @click="opened = true"
          style="width :50px; height : 50px; transform : translateX(335px) translateY(-10px)"
          v-show="!opened"
      />
      <span class="font-bold">Вагон {{ id }}</span>
    </div>
    <div class="details-container" v-show="opened">
      <div class="border-b-2 border-gray-300 pb-1">
        <div class="station-description">
          <span class="inline-block w-[60px]">Откуда:</span>
          <span class="station-name">{{ stations[0].name }}</span>
        </div>

        <div class="station-description">
          <span class="inline-block w-[60px]">Куда:</span>
          <span class="station-name">{{ stations[stations.length - 1].name }}</span>
        </div>

        <div class="station-description" v-if="distance > 0">
          <span class="inline-block w-[60px]">Длина:</span>
          <span class="station-name">{{ distance }} км</span>
        </div>
      </div>

      <div class="route-container">
        <div v-for="station in visibleStations" :key="station.id">
          <div class="flex items-center cursor-pointer">
            <div class="station-circle" @click="hideStations">
              <span style="position: relative; top: -6px" v-show="station.id === -1">...</span>
            </div>
            <span
                :class="[station.id !== -1 ? 'station-point-name' : 'ml-2']"
                @click="focusOnPoint(station)"
            >{{ station.name }}

            </span>

            <img
                v-show="station.id === -1"
                src="@/assets/images/dropdown.svg"
                class="stations-extend-icon"
                @click="extendStations"
            />
          </div>
          <div
              class="red-line"
              v-show="stations.indexOf(station) !== stations.length - 1 && !isAfk"
          ></div>
        </div>
      </div>

      <div
          class="afk-warning-container"
          v-show="isAfk"
      >ПРОСТАИВАЮЩИЙ ВАГОН!
      </div>
    </div>
  </div>

</template>

<script>

import interact from 'interactjs'

export default {
  props: ['id', 'stations', 'distance'],
  data() {
    return {
      opened: true,
      position: {x: -450, y: 10},
      visibleStations: [],
    }
  },
  mounted() {
    this.init();
  },
  watch: {
    stations() {
      this.init()
    }
  },
  methods: {
    init() {
      this.initInteraction();
      if (this.stations.length === 1) {
        this.stations.push(this.stations[0])
      }

      if (this.isAfk) {
        // afk wagon
        this.visibleStations = [this.stations[0]]
        return;
      }

      if (this.stations.length < 4) {
        this.visibleStations = this.stations
        return;
      }

      this.hideStations();
    },
    async focusOnPoint(station) {
      if (station.id === -1) {
        return;
      }

      await this.$emit('focusStation', station.latitude, this.longitude);
    },
    extendStations() {
      this.visibleStations = this.stations
    },
    hideStations() {
      if (this.hidedStations < 2) {
        return
      }

      this.visibleStations = [
        this.stations[0],
        this.extendPoint,
        this.stations[this.stations.length - 1]]
    },
    initInteraction() {
      let base = this;
      this.$refs.block.style.transform = `translate(${this.position.x}px, ${this.position.y}px)`

      interact(this.$refs.block).draggable({
        modifiers: [
          // interact.modifiers.restrict({
          //   restriction: 'parent',
          //   endOnly: true
          // })
        ],
        listeners: {
          start(event) {
          },
          move(event) {
            base.position.x += event.dx
            base.position.y += event.dy

            event.target.style.transform =
                `translate(${base.position.x}px, ${base.position.y}px)`
          },
        }
      })
    }
  },
  computed: {
    isAfk() {
      return this.stations.length === 2 && this.stations[0].id === this.stations[1].id
    },
    hidedStations() {
      return this.stations.length - 2
    },
    extendPoint() {
      return {
        id: -1,
        name: `+ ${this.hidedStations} станций`
      }
    }
  }
}

</script>

<style scoped>

.wagon-route-container {
  @apply w-[400px] bg-white rounded-xl border-2 border-[#E04434];
  @apply overflow-hidden absolute z-[20000];
}

.wagon-route-container .header {
  @apply w-full bg-[#E04434] text-center text-2xl text-white py-2;

}

.station-description {
  @apply px-3 py-1.5 text-gray-400;
}

.details-container {
  @apply w-full;
}

.details-container .station-name {
  @apply text-black ml-4  inline-block w-[270px] overflow-hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transform: translateY(6px);
}


.cross-icon {
  transform: translateX(350px) translateY(3px);
  @apply w-[25px] h-[25px] absolute cursor-pointer;
}

.route-container {
  @apply w-full p-3 max-h-[400px] overflow-y-scroll;
}

.stations-extend-icon {
  @apply ml-4 w-[25px]
}

.afk-warning-container {
  @apply w-full text-center text-2xl py-2 text-[#E04434] font-bold;
}

</style>
