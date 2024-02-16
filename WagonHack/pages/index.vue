<template>
  <div class="main-screen-container">
    <div class="map-container">
      <div id="map" style="width: 100%; height: 100%">
        <yandex-map
            ref="map"
            :settings="$store.state.settings"
            :coords="center"
            :bounds.sync="bounds"
            :zoom.sync="zoom"
            :controls="['fullscreenControl', 'zoomControl']"
            style="height : 100vh"
            @boundschange="getNewCenter"
            @map-was-initialized="mapLoaded"
        >

          <ymap-marker
              v-for="marker in currentMarkers"
              :coords="[marker.latitude, marker.longitude]"
              :marker-id="marker.id"
              marker-type="placemark"
              :key="marker.id"
              :balloon-template="balloonTemplate"
              @click="selectStationMarker(marker.id)"
              :options="{ iconLayout: 'default#image', iconImageHref: require('@/assets/images/station.svg')}"
          />
          <ymap-marker
              v-if="currentRoute"
              marker-id="current_route"
              marker-type="polyline"
              :options="{
              strokeColor: '#000000',
              strokeWidth: 5,
              strokeOpacity: 0.65
            }"
              :coords="routePoints"
          />
        </yandex-map>

      </div>
    </div>


    <transition name="opacity-transform">
      <div v-if="routePoints.length">
        <wagon-routes-modal
            :id="selectedWagonId"
            :stations="markers"
            :distance="distance"
        />
      </div>
    </transition>

    <div v-if="selectedStation.id">
      <station-info-modal
          :name="selectedStation.name"
          :wagons="selectedStation.wagons"
          :trains="selectedStation.trains"
      />
    </div>

    <div class="sidebar">


      <div class="w-full text-center bg-[#EB5525] py-4 text-white uppercase font-bold text-2xl">DataWagon</div>
      <div class="train-field">
        <img width="30" src="@/assets/images/search.svg"/>
        <input placeholder="Поезд\вагон\станция..." v-model="trainSearchValue"/>
      </div>

      <div class="divider"></div>

      <div class="flex items-center space-x-2 justify-center">
        <div class="flex space-x-1 items-center justify-center">
          <input type="checkbox" id="stations" v-model="showStations">
          <label for="stations">Станции</label>
        </div>
        <div class="flex space-x-1 items-center justify-center">
          <input type="checkbox" id="trains" v-model="showTrains">
          <label for="trains">Поезда</label>
        </div>
        <div class="flex space-x-1 items-center justify-center">
          <input type="checkbox" id="wagons" v-model="showWagons">
          <label for="wagons">Вагоны</label>
        </div>
      </div>

      <div class="divider mt-[2px]"></div>

      <div class="search-container">
        <div v-if="showStations">
          <station-item
              v-for="station in stations"
              :key="station.id"
              :trains="station.trains"
              :wagons="station.wagons"
              :longitude="station.longitude"
              :latitude="station.latitude"
              :name="station.name"
              :extended_prop="station.extended_prop"
              @stationFocus="focusOnMapObject"
              @closeTrainItem="closeTrainItem"
          />
        </div>

        <transition name="opacity-transform">
          <div v-if="searchResult">
            <div v-if="showTrains">
              <train-item
                  v-for="train in searchResult.trains"
                  :key="train.id"
                  :id="train.id"
                  :wagons="train.wagons"
                  :from="train['start_station']"
                  :to="train['end_station']"
                  :current="train['current_station']"
              />
            </div>

            <div v-if="showWagons">
              <div
                  v-for="wagon in searchResult.wagons"
                  :key="wagon.id"
              >
                <wagon-item
                    :id="wagon.id"
                    :train-id="wagon.trainId"
                    :current="wagon['current_station']"
                    :to="wagon['target_station']"
                    @closeWagonItem="hideWagonRoute"
                    @openWagonItem="showWagonRoute"
                />
              </div>
            </div>

          </div>
        </transition>


      </div>
    </div>
  </div>
</template>

<script>

import {loadYmap, yandexMap, ymapMarker} from 'vue-yandex-maps'

export default {
  name: 'IndexPage',
  components: {
    yandexMap, ymapMarker
  },
  data() {
    return {
      template_: {
        layout: 'default#image',
        imageHref: '@/assets/images/station.svg',
        imageSize: [43, 55],
        imageOffset: [-22, -55]
      },
      selectedWagonId: -1,
      trainSearchValue: '',
      searchResult: null,
      map: null,
      center: [55, 37],
      zoom: 10,
      bounds: [],
      markers: [], // stations on map
      stations: [],
      currentRoute: {}, // station items in sidebar
      oldMarkers: [],
      selectedStation: {},
      showStations: true,
      showTrains: true,
      showWagons: true,
      distance : 0
    }
  },
  async mounted() {
    this.setBounds(this.center);
    await loadYmap({...this.$store.state.settings, debug: true});

    // this.markers = await this.getStations() // stations
    this.markers = await this.getStations();
  },
  computed: {
    balloonTemplate() {
      return `
      <h1 class="text-2xl">${this.selectedStation.name}</h1>
    `
    },
    routePoints() {
      if (!this.currentRoute || !this.currentRoute.path) {
        return []
      }

      const res = []
      for (let i = 0; i < this.currentRoute.path.length; i++) {
        const item = this.currentRoute.path[i]
        const station = this.currentRoute.stations[item]
        if (station) {
          res.push([station.latitude, station.longitude])
        }
      }

      return res
    },
    currentMarkers() {
      if (this.ifDict(this.currentRoute) && this.zoom < 9) {
        return []
      }

      return this.markers
    }
  },
  methods: {
    closeTrainItem() {
      this.selectedStation = {}
    },
    ifDict(dict) {
      return Object.keys(dict).length
    },
    async hideWagonRoute() {
      console.log('ЗАКРЫВАЕМСЯ НА ОБЕДЕННЫЙ ПЕРЕРЫВ')
      this.currentRoute = {}
      this.routePoints = []
      this.selectedWagonId = -1
      this.distance = 0

      this.markers = await this.getStations();

    },
    async showWagonRoute(from, to, id) {
      let urlArgs = `?from=${from.id}&to=${to.id}`

      this.currentRoute = await this.$axios.$get(this.$store.state.api + 'build_route' + urlArgs);

      if (!this.currentRoute.path) {
        alert('ути пути нет маршрута((((((((')
        return
      }
      this.markers = [];
      this.selectedWagonId = id;
      this.distance = this.currentRoute['path_cost']
      console.log('DISTANCE', this.distance);

      let stations = this.currentRoute.stations;
      let ids = Object.keys(stations)
      let station = stations[ids[0]]

      this.focusOnMapObject(this.routePoints[0], station.name, station.trains, station.wagons)
      for (let i = 0; i < this.currentRoute.path.length; i++) {
        const item = this.currentRoute.path[i]
        const station = this.currentRoute.stations[item]

        if (station) {
          this.markers.push(station);
        }
      }
    },
    setBounds(center) {
      this.bounds = [[center[0] - .5, center[1] - .5], [center[0] + .5, center[1] + .5]]
    },
    selectStationMarker(stationId) {
      if (stationId.length > 10) {
        // buggy: if marker is grouped (clustering)
        this.selectedStation.name = "Группа маркеров"
        return
      }

      let station = this.markers.filter(item => item.id === stationId)
      if (!station.length) {
        return
      }

      let toAdd = station[0]
      toAdd.extended_prop = true
      this.selectedStation = toAdd;

      if (this.stations.includes(toAdd) || this.stations.filter(item => item.id === toAdd.id).length) {
        return;
      }

      this.stations = [toAdd, ...this.stations]
    },
    focusOnMapObject(value, stationName, stationTrains, stationWagons) {
      this.selectedStation = {
        id: 666,
        name: stationName,
        trains: stationTrains,
        wagons: stationWagons
      }

      this.center = value;
      this.setBounds(value);
      setTimeout(() => {
        this.zoom = 15;
      }, 1000)

    },
    async mapLoaded(event) {
      this.bounds = [event._bounds[0], event._bounds[1]]

      // this.currentRoute = await this.$axios.$get(this.$store.state.api + '/build_route?from=415&to=640')
    },
    getNewCenter(event) {
      this.center = event.get('newCenter')
      // this.bounds = event.get('newBounds')
      // this.zoom = event.get('newZoom')
    },
    async getStations() {
      if (Object.keys(this.currentRoute).length) {
        return this.markers;
      }

      let url = `${this.$store.state.api}/stations?`
      url += `latitude1=${this.bounds[0][0]}&`
      url += `latitude2=${this.bounds[1][0]}&`
      url += `longitude1=${this.bounds[0][1]}&`
      url += `longitude2=${this.bounds[1][1]}&`
      url += `zoom=${this.zoom}`

      return await this.$axios.$get(url)
    },
  },
  watch: {
    markers(value) {
    },
    zoom(value) {
      if (value < 10 && !this.ifDict(this.currentRoute)) {
        setTimeout(() => {
          this.zoom = 10;
        }, 0)
      }
      if (value < 8 && this.ifDict(this.currentRoute)) {
        // this.oldMarkers = this.markers
        // this.markers = []
      }
    },
    searchResult(val) {
      if (!val) {
        return
      }

      this.stations = val.stations
    },
    async center(newValue, oldValue) {
      // if (Math.abs(newValue[0] - oldValue[0]) > 0.05
      //     || Math.abs(newValue[1] - oldValue[1]) > 0.05) {
      this.markers = await this.getStations()
      // }
    },
    async trainSearchValue(val) {
      if (!val) {
        this.searchResult = null;
        return
      }

      this.searchResult = await this.$axios.$get(this.$store.state.api + `/search?q=${val}`)
    }
  }
}
</script>

<style scoped>

.train-field {
  @apply w-[90%] flex mx-auto border-2 border-[rgba(0,0,0,16%)] px-3 py-1;
  @apply rounded-3xl my-4;
}

.train-field input {
  @apply outline-none px-3 py-2 rounded-md w-full;
}

.search-container {
  @apply h-[78%] overflow-y-scroll;

}

</style>
