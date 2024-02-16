<template>
  <div class="station-info-container" ref="block">
    <div class="header" @click.self="extended = !extended">
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

        <img
            class="cross-icon"
            src="@/assets/images/crossWhite.svg"
            @click="extended = false"
            v-show="extended"
        />
        <img
            class="cross-icon"
            src="@/assets/images/dropdownWhite.svg"
            @click="extended = true"
            style="width :50px; height : 50px; transform : translateX(170px) translateY(-10px)"
            v-show="!extended"
        />
      </div>
    </div>

    <div v-show="extended">
      <div class="station-description">{{ name }}</div>

      <div class="flex items-center space-x-2 justify-center border-b-2 border-gray-400 py-2">
        <div class="flex space-x-1 items-center justify-center">
          <input type="checkbox" id="trains" v-model="showTrains" class="w-[20px] h-[20px]">
          <label for="trains">Поезда</label>
        </div>
        <div class="flex space-x-1 items-center justify-center">
          <input type="checkbox" id="wagons" v-model="showWagons" class="w-[20px] h-[20px]">
          <label for="wagons">Вагоны</label>
        </div>
      </div>

      <div class="details-container" v-show="!currentSection">
        <span v-show="!trains.length">Нет свободных поездов</span>

        <div v-show="showTrains">
          <train-item
              v-for="train in freeTrains"
              :key="train.id"
              :id="train.id"
              :from="train['start_station']"
              :to="train['end_station']"
              :current="train['current_station']"
              :wagons="train.wagons"
          />
        </div>

        <div v-show="showWagons">
          <wagon-item
              v-for="wagon in freeWagons"
              :key="wagon.id"
              :id="wagon.id"
              :train-id="wagon['train_id']"
              :to="wagon['target_station']"
              :current="wagon['current_station']"
          />
        </div>
      </div>

      <div class="details-container" v-show="currentSection">
        <div v-show="showTrains">
          <train-item
              v-for="train in busyTrains"
              :key="train.id"
              :id="train.id"
              :from="train['start_station']"
              :to="train['end_station']"
              :current="train['current_station']"
              :wagons="train.wagons"
          />
        </div>

        <div v-show="showWagons">
          <wagon-item
              v-for="wagon in busyWagons"
              :key="wagon.id"
              :id="wagon.id"
              :train-id="wagon['train_id']"
              :to="wagon['target_station']"
              :current="wagon['current_station']"
          />
        </div>
      </div>
    </div>

  </div>

</template>

<script>

import interact from "interactjs";

export default {
  props: ['id', 'name', 'trains', 'wagons'],
  data() {
    return {
      position: {
        x: -900,
        y: 10
      },
      currentSection: 0,
      busyTrains: [],
      freeTrains: [],
      busyWagons: [],
      freeWagons: [],
      showTrains: true,
      showWagons: true,
      extended: true
    }
  },
  mounted() {
    this.init();
  },
  watch: {
    trains() {
      this.init();
    },
  },
  methods: {
    init() {
      this.initInteraction()

      this.freeTrains = this.trains.filter(item => item['current_station_id'] === item['end_station_id'])
      this.busyTrains = this.trains.filter(item => item['current_station_id'] !== item['end_station_id'])

      this.freeWagons = this.wagons.filter(item => item['current_station_id'] === item['target_station_id'])
      this.busyWagons = this.wagons.filter(item => item['current_station_id'] !== item['target_station_id'])
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
  @apply w-full bg-[#E04434] text-center text-lg text-white py-1.5 cursor-pointer;
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

.details-container {
  @apply max-h-[400px] overflow-y-auto;
}

.station-description {
  @apply px-3 py-1.5 text-gray-500 border-b-2 border-gray-400;
}

.details-container {
  @apply px-2 py-1;
}

.cross-icon {
  transform: translateX(170px) translateY(3px);
  @apply w-[22px] h-[22px] absolute cursor-pointer;
}

</style>
