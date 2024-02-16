<template>
  <div class="station-info-container" ref="block">
    <div class="header">
      <div class="header-content">
        <div
            :class="['switcher', !currentSection ? 'underline' : '']"
            @click="currentSection = 0"
        >Свободные
        </div>
        <div
            :class="['switcher', currentSection ? 'underline' : '']"
            @click="currentSection = 1"
        >Занятые
        </div>
      </div>
    </div>

    <div class="station-description">Станция норме пидарас</div>
    <div class="details-container" v-show="!currentSection">

    </div>

    <div class="details-container" v-show="currentSection">
      занятые
    </div>
  </div>

</template>

<script>

import interact from "interactjs";

export default {
  data() {
    return {
      position: {
        x: 0,
        y: 10
      },
      currentSection: 0,
      trains: [
        {
          id: 1,
          start_station_id: 3,
          end_station_id: 3
        },
        {
          id: 2,
          start_station_id: 2,
          end_station_id: 3
        },
        {
          id: 3,
          start_station_id: 2,
          end_station_id: 2
        },
        {
          id: 4,
          start_station_id: 2,
          end_station_id: 34
        }
      ],
      wagons: [
        {
          id: 1,
          current_station_id: 2,
          target_station_id: 3,
        },
        {
          id: 2,
          current_station_id: 3,
          target_station_id: 3,
        },
        {
          id: 3,
          current_station_id: 2,
          target_station_id: 3,
        },
        {
          id: 4,
          current_station_id: 3,
          target_station_id: 3,
        }
      ],
      busyTrains: [],
      freeTrains: [],
      busyWagons: [],
      freeWagons: []
    }
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.initInteraction()

      this.busyTrains = this.trains.filter(item => item['start_station_id'] === item['end_station_id'])
      this.freeTrains = this.trains.filter(item => item['start_station_id'] !== item['end_station_id'])

      this.busyWagons = this.wagons.filter(item => item['current_station_id'] === item['target_station_id'])
      this.freeWagons = this.wagons.filter(item => item['current_station_id'] !== item['target_station_id'])
    },
    initInteraction() {
      let base = this;
      this.$refs.block.style.transform = `translate(${this.position.x}px, ${this.position.y}px)`

      interact(this.$refs.block).draggable({
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
  }
}

</script>

<style scoped>

.station-info-container {
  @apply w-[400px] bg-white rounded-xl border-2 border-[#E04434];
  @apply overflow-hidden absolute z-[20000];
}

.station-info-container .header {
  @apply w-full bg-[#E04434] text-center text-lg text-white py-1;
}

.station-info-container .header .header-content {
  @apply grid grid-cols-2 justify-items-center w-full;
}


.switcher {
  @apply cursor-pointer;
}

.switcher:hover {
  @apply underline ;
}


.station-description {
  @apply px-3 py-1.5 text-gray-500 border-b-2 border-gray-400;
}

.details-container {
  @apply px-2 py-1;
}

</style>
