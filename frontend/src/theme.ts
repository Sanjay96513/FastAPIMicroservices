import { extendTheme, type ThemeConfig } from '@chakra-ui/react'

const config: ThemeConfig = {
  initialColorMode: 'dark', // Set dark mode as the default
  useSystemColorMode: false,
}

const theme = extendTheme({ config })

export default theme