<template>
  <Popover
    as="header"
    class="pb-16 bg-primary dark:bg-sky-900"
    v-slot="{ open }"
  >
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="relative py-3 flex items-center justify-center lg:justify-between">
        <!-- Logo -->
        <div class="absolute left-0 flex-shrink-0 lg:static">
          <a href="#">
            <span class="sr-only">BairesDev</span>
            <img
              class="block lg:hidden h-8 w-auto "
              src="../../assets/bairesdev-icon-white.svg"
              alt="BairesDev"
            />
            <img
              class="hidden lg:block h-8 w-auto "
              src="../../assets/bairesdev-tt-logo-white.svg"
              alt="BairesDev"
            />
          </a>
        </div>

        <!-- Right section on desktop -->
        <div class="hidden lg:ml-4 lg:flex lg:items-center lg:pr-0.5">
          <div class="ml-3 min-w-0 text-white">
            <div v-if="actAsPM" class="text-base font-medium truncate">
              {{ $store.state.PMUser.name }}
              <span class="text-sm opacity-75 italic">ID 4522 (BP)</span>
            </div>
            <div v-else class="text-base font-medium truncate">
              {{ $store.state.loginUser.user.name }}
              <span class="text-sm opacity-75 italic">ID 3332 (BP)</span>
            </div>
            <div v-if="actAsPM" class="text-sm font-medium opacity-60 truncate">{{ $store.state.PMUser.email }}</div>
            <div v-else class="text-sm font-medium opacity-60 truncate">{{ $store.state.loginUser.user.email }}</div>
          </div>
          <!-- Profile dropdown -->
          <Menu
            as="div"
            class="ml-4 relative flex-shrink-0"
          >
            <div>
              <MenuButton class="bg-white rounded-full flex text-sm ring-2 ring-white ring-opacity-20 focus:outline-none focus:ring-opacity-100">
                <span class="sr-only">Open user menu</span>
                <img
                  class="h-8 w-8 rounded-full"
                  :src="actAsPM ?  $store.state.PMUser.avatar : $store.state.loginUser.user.profileImage"
                  alt=""
                />
              </MenuButton>
            </div>
            <transition
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems class="origin-top-right z-40 absolute -right-2 mt-2 w-64 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                <MenuItem v-if="!actAsPM" v-slot="{ active }">
                <a
                    @click.prevent="setPMInterface"
                    href="#"
                    :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']"
                  >Act as PM (Demo purpose)</a>
                </MenuItem>
                <MenuItem v-else v-slot="{ active }">
                <a
                    @click.prevent="removePMInterface"
                    href="#"
                    :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']"
                  >Act as a regular user</a>
                </MenuItem>
                <MenuItem v-if="!darkMode" v-slot="{ active }">
                <a
                    @click.prevent="activateDarkMode"
                    href="#"
                    :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']"
                  >Dark Mode</a>
                </MenuItem>
                <MenuItem v-else v-slot="{ active }">
                <a
                    @click.prevent="deactivateDarkMode"
                    href="#"
                    :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']"
                  >Light Mode</a>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                <a
                  @click.prevent="logout"
                  href="#"
                  :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']"
                >Sign out</a>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
        </div>

        <div class="flex-1 min-w-0 px-12 lg:hidden">
          <div class="max-w-xs w-full mx-auto text-white font-bold">
            Time Tracker
          </div>
        </div>

        <!-- Menu button -->
        <div class="absolute right-0 flex-shrink-0 lg:hidden">
          <!-- Mobile menu button -->
          <PopoverButton class="bg-transparent p-2 rounded-md inline-flex items-center justify-center text-sky-200 hover:text-white hover:bg-white hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-white">
            <span class="sr-only">Open main menu</span>
            <MenuIcon
              v-if="!open"
              class="block h-6 w-6"
              aria-hidden="true"
            />
            <XIcon
              v-else
              class="block h-6 w-6"
              aria-hidden="true"
            />
          </PopoverButton>
        </div>
      </div>
      <div class="hidden lg:block py-3">

      </div>
    </div>

    <TransitionRoot
      as="template"
      :show="open"
    >
      <div class="lg:hidden">
        <TransitionChild
          as="template"
          enter="duration-150 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <PopoverOverlay
            static
            class="z-20 fixed inset-0 bg-black bg-opacity-25"
          />
        </TransitionChild>

        <TransitionChild
          as="template"
          enter="duration-150 ease-out"
          enter-from="opacity-0 scale-95"
          enter-to="opacity-100 scale-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100 scale-100"
          leave-to="opacity-0 scale-95"
        >
          <PopoverPanel
            focus
            static
            class="z-30 absolute top-0 inset-x-0 max-w-3xl mx-auto w-full p-2 transition transform origin-top"
          >
            <div class="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white divide-y divide-gray-200">
              <div class="pt-3 pb-2">
                <div class="flex items-center justify-between px-4">
                  <div>
                    <img
                      class="h-8 w-auto"
                      src="../../assets/bairesdev-tt-logo-blue.svg"
                      alt="BairesDev"
                    />
                  </div>
                  <div class="-mr-2">
                    <PopoverButton class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-sky-500">
                      <span class="sr-only">Close menu</span>
                      <XIcon
                        class="h-6 w-6"
                        aria-hidden="true"
                      />
                    </PopoverButton>
                  </div>
                </div>
                <div class="mt-3 px-2 space-y-1">
                  <router-link
                    v-for="(option,index) in options"
                    :key="index"
                    :to="option.href"
                    class="border-transparent hover:border-gray-300 hover:text-gray-800 block border-l-4 px-3 py-2 text-base text-gray-900 font-medium hover:bg-gray-100"
                    aria-current="page"
                    exact-active-class="bg-sky-50 border-sky-500 text-sky-700"
                  >{{ option.title }}</router-link>
                </div>
              </div>
              <div class="pt-4 pb-2">
                <div class="flex items-center px-5">
                  <div class="flex-shrink-0">
                    <img
                      class="h-10 w-10 rounded-full"
                      :src="actAsPM ? $store.state.PMUser.avatar : $store.state.loginUser.user.profileImage"
                      alt=""
                    />
                  </div>
                  <div class="ml-3 min-w-0 flex-1">
                    <div v-if="actAsPM" class="text-base font-medium text-gray-800 truncate">
                      {{ $store.state.PMUser.name }}
                      <span>4325</span>
                    </div>
                    <div class="text-base font-medium text-gray-800 truncate">
                      {{ $store.state.loginUser.user.name }}
                      <span>2354</span>
                    </div>
                    <div v-if="actAsPM" class="text-sm font-medium text-gray-500 truncate">{{ $store.state.PMUser.email }}</div>
                    <div v-else class="text-sm font-medium text-gray-500 truncate">{{ $store.state.loginUser.user.email }}</div>
                  </div>
                </div>
                <div class="mt-3 px-2 space-y-1">
                  <a v-if="actAsPM"
                    @click.prevent="removePMInterface"
                    href="#"
                    class="block rounded-md px-3 py-2 text-base text-gray-900 font-medium hover:bg-gray-100 hover:text-gray-800"
                  >Act as a regular user</a>
                  <a v-else
                    @click.prevent="setPMInterface"
                    href="#"
                    class="block rounded-md px-3 py-2 text-base text-gray-900 font-medium hover:bg-gray-100 hover:text-gray-800"
                  >Act as PM (Demo purpose)</a>
                  <a
                    @click.prevent="setPMInterface"
                    href="#"
                    class="block rounded-md px-3 py-2 text-base text-gray-900 font-medium hover:bg-gray-100 hover:text-gray-800"
                  >Sign out</a>
                </div>
              </div>
            </div>
          </PopoverPanel>
        </TransitionChild>
      </div>
    </TransitionRoot>
  </Popover>
</template>

<script>
import {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    Popover,
    PopoverButton,
    PopoverOverlay,
    PopoverPanel,
    TransitionChild,
    TransitionRoot,
} from '@headlessui/vue'
import { MenuIcon, XIcon } from '@heroicons/vue/outline'
import { mapState, mapMutations, mapActions } from 'vuex'


export default {
    components: {
        Menu,
        MenuButton,
        MenuItem,
        MenuItems,
        Popover,
        PopoverButton,
        PopoverOverlay,
        PopoverPanel,
        TransitionChild,
        TransitionRoot,
        MenuIcon,
        XIcon,
    },
    computed: {
        ...mapState({
            actAsPM: (state) => state.actAsPM,
            darkMode: (state) => state.darkMode,
        }),
    },
    methods: {
      ...mapActions(['setDarkMode']),
        logout() {
            this.$store.commit('removeLoginUser')
            this.$router.push('/login')
        },
        activateDarkMode(){
          this.setDarkMode(true)
        },
        deactivateDarkMode(){
          this.setDarkMode(false)
        },
        ...mapMutations(['setPMInterface', 'removePMInterface']),
    },
}
</script>
