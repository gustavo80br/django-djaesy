<template>
  <div class="min-h-screen bg-white flex">
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img
            class="h-12 w-auto"
            src="../../assets/bairesdev-logo-blue.svg"
            alt="BairesDev"
          />
          <h2 class="mt-6 text-2xl font-extrabold text-gray-500">
            Time Tracker
          </h2>
          <p class="mt-2 text-sm text-gray-600">
            You should use your BairesDev email account to access this platform.
          </p>
        </div>

        <div class="mt-8">
          <div>
            <div class="flex items-center justify-around">
              <p class="text-sm font-medium text-blue-400">
                Sign in with
              </p>
              <div class="mt-1 w-36">
                <div>
                  <a
                    @click.prevent="googleLogin"
                    href="#"
                    class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Sign in with Google</span>
                    <span class="w-5 h-5"><i class="fab fa-google"></i></span>
                  </a>
                </div>
              </div>
            </div>
            <div class="mt-6 relative">
              <div
                class="absolute inset-0 flex items-center"
                aria-hidden="true"
              >
                <div class="w-full border-t border-gray-300"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white text-gray-500">
                  Need some help?
                </span>
              </div>
            </div>
          </div>
          <div class="mt-6 relative">
            <p class="mt-2 text-sm text-gray-600">
              If you have any problem, raise a Support Request in <a
                class="text-blue-500"
                href="https://bairesdev.atlassian.net/servicedesk"
              >Service Desk</a>.
            </p>
            <p class="mt-2 text-sm text-gray-600">
              If you want to change your password, <a
                class="text-blue-500"
                href="https://timetracker.bairesdev.com/CambiarClave.aspx"
              >click here</a>.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="hidden lg:block relative w-0 flex-1">
      <img
        class="absolute inset-0 h-full w-full object-cover"
        src="https://images.unsplash.com/photo-1505904267569-f02eaeb45a4c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1908&q=80"
        alt=""
      />
    </div>
  </div>
</template>
<script>
export default {
    methods: {
        googleLogin() {
            this.$gAuth
                .signIn()
                .then((GoogleUser) => {
                    const userInfo = {
                        auth: GoogleUser.getAuthResponse(),
                        user: {
                            name: GoogleUser.getBasicProfile().getName(),
                            email: GoogleUser.getBasicProfile().getEmail(),
                            profileImage:
                                GoogleUser.getBasicProfile().getImageUrl(),
                        },
                    }
                    this.$store.commit('setLoginUser', userInfo)
                    this.$router.push('/')
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        async handleClickSignIn() {
            try {
                const googleUser = await this.$gAuth.signIn()
                if (!googleUser) {
                    return null
                }
                console.log('googleUser', googleUser)
                this.user = googleUser.getBasicProfile().getEmail()
                console.log('getId', this.user)
                console.log('getBasicProfile', googleUser.getBasicProfile())
                console.log('getAuthResponse', googleUser.getAuthResponse())
                console.log(
                    'getAuthResponse',
                    this.$gAuth.instance.currentUser.get().getAuthResponse()
                )
            } catch (error) {
                //on fail do something
                console.error(error)
                return null
            }
        },
        async handleClickGetAuthCode() {
            try {
                const authCode = await this.$gAuth.getAuthCode()
                console.log('authCode', authCode)
            } catch (error) {
                console.error(error)
                return null
            }
        },
        async handleClickSignOut() {
            try {
                await this.$gAuth.signOut()
                console.log('isAuthorized', this.Vue3GoogleOauth.isAuthorized)
                this.user = ''
            } catch (error) {
                console.error(error)
            }
        },
        handleClickDisconnect() {
            window.location.href = `https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=${window.location.href}`
        },

    },
}
</script>
