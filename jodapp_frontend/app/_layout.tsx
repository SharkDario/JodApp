// app/_layout.tsx (Layout principal)
import { Slot } from 'expo-router';
import { AuthProvider } from '../context/AuthContext';
import { useAuth } from '../context/AuthContext';
import FlashMessage from 'react-native-flash-message';
import { useEffect } from 'react';
import { router } from 'expo-router';

function RootLayoutContent() {
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        router.replace('/(usuario_autenticado)');
      } else {
        router.replace('/(publico)');
      }
    }
  }, [isAuthenticated, isLoading]);

  return <Slot />;
}

export default function RootLayout() {
  return (
    <AuthProvider>
      <RootLayoutContent />
      <FlashMessage position="top" />
    </AuthProvider>
  );
}

/*
import { Slot, Redirect } from 'expo-router';
import { useAuth } from '../context/AuthContext'; // Deberás crear este contexto

export default function RootLayout() {
  // Este layout principal solo decide si mostrar el drawer o las rutas protegidas
  const { isAuthenticated } = useAuth();
  
  // Si está autenticado, redirige a la ruta principal de usuario autenticado
  if (isAuthenticated) {
    return <Redirect href="/usuario_autenticado" />;
  }

  // Si no está autenticado, muestra el drawer público
  return <Slot />;
}*/