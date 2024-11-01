//app/(publico)/_layout.tsk
import { Drawer } from 'expo-router/drawer';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Colors } from '@/constants/Colors';
import { TabBarIcon } from '@/components/navigation/TabBarIcon';
import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { router } from 'expo-router';

export default function PublicLayout() {
  const colorScheme = useColorScheme();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      router.replace('/(usuario_autenticado)');
    }
  }, [isAuthenticated]);

  return (
    <Drawer
      screenOptions={{
        drawerActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        drawerInactiveTintColor: colorScheme === 'dark' ? '#fff' : '#000',
        drawerStyle: {
          backgroundColor: Colors[colorScheme ?? 'light'].background,
        },
        headerStyle: {
          backgroundColor: Colors[colorScheme ?? 'light'].background,
        },
        headerTintColor: colorScheme === 'dark' ? '#fff' : '#000',
      }}
    >
      <Drawer.Screen
        name="index"
        options={{
          title: 'Home',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="login"
        options={{
          title: 'Iniciar sesión',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'log-in' : 'log-in-outline'} color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="signup"
        options={{
          title: 'Registro',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'person-add' : 'person-add-outline'} color={color} size={size} />
          ),
        }}
      />
    </Drawer>
  );
}
/*
import { Drawer } from 'expo-router/drawer';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Colors } from '@/constants/Colors';
import { TabBarIcon } from '@/components/navigation/TabBarIcon';

export default function DrawerLayout() {
  const colorScheme = useColorScheme();

  return (
    <Drawer
      screenOptions={{
        drawerActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        drawerInactiveTintColor: colorScheme === 'dark' ? '#fff' : '#000',
        drawerStyle: {
          backgroundColor: Colors[colorScheme ?? 'light'].background,
        },
        headerStyle: {
          backgroundColor: Colors[colorScheme ?? 'light'].background,
        },
        headerTintColor: colorScheme === 'dark' ? '#fff' : '#000',
      }}
    >
      <Drawer.Screen
        name="index"  // Name must match the file name "index.tsx"
        options={{
          title: 'Home',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="login"  // Name must match the file name "login.tsx"
        options={{
          title: 'Inicio de sesión',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'log-in' : 'log-in-outline'} color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="signup"  // Name must match the file name "signup.tsx"
        options={{
          title: 'Registro',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'person-add' : 'person-add-outline'} color={color} size={size} />
          ),
        }}
      />
    </Drawer>
  );
}
*/