<template>
  <div class="wrapper">
    <div class="train-container" @click="extended ? hide() : extend()">
      <div class="flex w-[90%]">
        <img src="@/assets/images/train.svg" class="mr-4"/>
        <span class="truncate"><b>{{ id }}</b> (<span class="italic">{{ from.name }} → {{ to.name }}</span>)</span>
      </div>
      <img
        src="@/assets/images/dropdown.svg"
        width="20"
        v-show="!extended"
      />
      <img
        src="@/assets/images/cross.svg"
        width="20"
        v-show="extended"
      />
    </div>

    <div class="details-container" v-show="extended">
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

<!--      <div class="divider mt-5"></div>-->

<!--      <span>Информация о вагонах:</span>-->

<!--      <div-->
<!--        class="mt-2 px-3 py-1 rounded-lg cursor-pointer bg-[#D9D9D9] w-fit"-->
<!--        @click="showWagonModal = true"-->
<!--      >Подробнее-->
<!--      </div>-->


      <div
        class="wagon-modal-container"
        v-show="showWagonModal"
        @click.self="showWagonModal = false"
      >
        <div class="wagon-modal">
          <div class="header">ВАГОНЫ</div>

<!--          <wagon-item-->
<!--            v-for="type in wagonTypes"-->
<!--            :key="type"-->
<!--            :wagon-type="type"-->
<!--            :cars = "train['cars'].filter(item => item.type === type)"-->
<!--          />-->
        </div>
      </div>

    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      extended: false,
      stations: [],
      visibleStations: [],
      wagonTypes: new Set(),
      showWagonModal: false,
    }
  },
  props: ['id', 'wagons', 'from', 'to', 'current'],
  methods: {
    extend() {
      this.extended = true
    },
    hide() {
      this.extended = false
    }
  },
  async mounted() {
    this.stations = [this.from,  { id: -1, name : '...' }, this.current]
    if (this.current !== this.to) {
      this.stations.push({ name : '...' })
      this.stations.push(this.to);
    }
  },
}

</script>


<style scoped>

.train-container {
  @apply px-4 py-3 w-full bg-[#FEF4F4] mb-1 flex;
  @apply cursor-pointer items-center;
}

.train-container span {
  @apply w-[90%]
}

.train-container img {
  @apply cursor-pointer;
}

.details-container {
  @apply w-full px-4 pt-4 pb-5;
}



.wagon-modal-container {
  @apply backdrop-blur-2xl w-screen h-screen absolute left-0 top-0;
  @apply text-white;
}

.wagon-modal {
  @apply bg-white w-[450px] mx-auto rounded-lg mt-[200px] shadow-2xl;
  @apply h-[60%] overflow-y-scroll;
}

.wagon-modal .header {
  @apply bg-red-600 w-full py-4 rounded-t-lg text-center font-bold;
}

</style>
