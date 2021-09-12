<template>
  <div :class="[this.$store.state.darkMode ?'dark bg-gray-900' :'bg-gray-100','min-h-screen ']">
    <navigation v-if="this.$store.state.loginUser"></navigation>
    <main :class="[!this.$store.state.loginUser?'':'-mt-20',' pb-8']">
      <pm-screen v-if="actAsPM"></pm-screen>
      <router-view v-else />
    </main>
    <footer v-if="this.$store.state.loginUser">
      <div class="container mx-auto">
        <div class="border-t border-gray-200 py-8 text-sm text-gray-500 dark:text-gray-50 text-center"><span class="block sm:inline">&copy; BairesDev 2009 – 2021. All rights reserved.</span></div>
      </div>
    </footer>
  </div>
</template>


<script>
import Navigation from './components/navigation/Navigation.vue';
import PmScreen from './components/views/PmScreen.vue';
import { mapState } from 'vuex'

export default {
  name: 'app',
  components: { Navigation,PmScreen },
  computed: {
        ...mapState({
            actAsPM: (state) => state.actAsPM,
        }),
    },
};
</script>
