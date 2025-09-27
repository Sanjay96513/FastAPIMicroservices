import {
  ChakraProvider,
  Box,
  VStack,
  Grid,
  theme,
  Heading,
  Button,
  useColorMode,
  Container,
  Text,
} from "@chakra-ui/react";

function ColorModeSwitcher() {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <Button onClick={toggleColorMode}>
      Toggle {colorMode === "light" ? "Dark" : "Light"}
    </Button>
  );
}

export default function App() {
  return (
    <Box textAlign="center" fontSize="xl">
      <Grid minH="100vh" p={3}>
        <VStack spacing={8}>
          <Container maxW="container.lg">
            <Heading as="h1" size="xl" my={4}>
              FastAPI + React Microservices Template
            </Heading>
            <Text>
              This is the starting point for the React frontend.
            </Text>
            <ColorModeSwitcher />
            {/* Placeholder for Login Form or Dashboard */}
            <Box mt={8} p={4} borderWidth={1} borderRadius="lg">
              <Heading as="h2" size="lg">Application Content</Heading>
              <Text mt={2}>
                A login form, user dashboard, or other components would be rendered here.
              </Text>
            </Box>
          </Container>
        </VStack>
      </Grid>
    </Box>
  );
}