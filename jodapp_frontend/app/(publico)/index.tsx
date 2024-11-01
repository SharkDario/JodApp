import { Image, StyleSheet, View, Text, Linking, TouchableOpacity, Dimensions, Platform, Button, ImageBackground } from 'react-native';
import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/FontAwesome'; // Import FontAwesome icons
import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';

import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
//import HoverCard from '@/components/HoverCard';
import ParallaxCarousel from '@/components/ParallaxCarousel';


export default function HomeScreen() {
    const router = useRouter();
    const windowWidth = Dimensions.get('window').width;
    // Updated data array
    const myData = [
      {
        title: '',
        image: 'azul_roxo',
        frontText: 'Experiencia Inolvidable',
        backText: 'Noches llenas de ritmo',
      },
      {
        title: '',
        image: 'club_3',
        frontText: 'Reserva tu Noche Perfecta',
        backText: 'Asegura tu mesa en el mejor ambiente',
      },
      {
        title: '',
        image: 'club_1',
        frontText: 'Descubre la Magia Nocturna',
        backText: 'Eventos exclusivos y sorpresas cada semana.',
      },
      {
        title: '',
        image: 'club_2',
        frontText: 'Vive el momento',
        backText: 'Déjate llevar',
      },
    ];

    const openLink = (url) => {
      Linking.openURL(url);
    };


    return (
        <ParallaxScrollView
            headerBackgroundColor={{ light: 'transparent', dark: 'transparent' }}
            headerImage={
              <View style={{ width: windowWidth, height: 250 }}>
                  <ImageBackground
                        source={require('@/assets/images/fondo_morado.jpg')}
                        style={{ width: '100%', height: '100%' }}
                    ></ImageBackground>
                  {/* Logo Overlay */}
                  <Image
                      source={require('@/assets/images/jodapp-logo.png')}
                      style={styles.logoOverlay}
                  />
              </View>
          }>
            
            <ThemedView style={styles.titleContainer}>
                <ThemedText type="title">¡Bienvenid@ a JodApp!</ThemedText>
                <HelloWave />
            </ThemedView>

            <ParallaxCarousel data_arg={myData}></ParallaxCarousel>
            <Text style={styles.link} onPress={() => router.push('/login')}>
                ¿Tienes una cuenta? Entrar
            </Text>
            {/* Footer */}
            <View style={styles.footer}>
                <View style={styles.iconContainer}>
                    <TouchableOpacity onPress={() => openLink('https://www.instagram.com/sharkdario')}>
                        <Icon name="instagram" size={30} color="#E1306C" />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://www.youtube.com/@DarioCoronel07')}>
                        <Icon name="youtube" size={30} color="#FF0000" />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://github.com/SharkDario/JodApp')}>
                        <Icon name="github" size={30} color="#FFFFFF" />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://www.linkedin.com/in/dariocoronel/')}>
                        <Icon name="linkedin" size={30} color="#0077B5" />
                    </TouchableOpacity>
                </View>
                <Text style={styles.copyright}>© 2024 JodApp from SharkDario</Text>
            </View>
        </ParallaxScrollView>
    );
}

const styles = StyleSheet.create({
    titleContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        marginBottom: 30,
    },
    stepContainer: {
        gap: 8,
        marginBottom: 8,
    },
    reactLogo: {
        height: 178,
        width: 290,
        bottom: 0,
        left: 0,
        position: 'absolute',
    },
    logoOverlay: {
      position: 'absolute',
      width: 250,
      height: 250,
      top: '50%',
      left: '50%',
      transform: [{ translateX: -125 }, { translateY: -125 }],
      resizeMode: 'contain',
    },
    footer: {
      alignItems: 'center',
      marginTop: 0,
      paddingVertical: 10,
      backgroundColor: '#7C03D6',
      borderRadius: 10,
    },
    iconContainer: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        width: '60%',
        marginBottom: 10,
    },
    copyright: {
        fontSize: 14,
        color: '#FFFFFF',
    },
    link: {
      marginTop: 0,
      textAlign: 'center',
      color: 'white',
      textDecorationLine: 'underline',
    },
});


/*
import { Image, StyleSheet, Platform } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
        />
      }>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Welcome!</ThemedText>
        <HelloWave />
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Step 1: Try it</ThemedText>
        <ThemedText>
          Edit <ThemedText type="defaultSemiBold">app/(tabs)/index.tsx</ThemedText> to see changes.
          Press{' '}
          <ThemedText type="defaultSemiBold">
            {Platform.select({ ios: 'cmd + d', android: 'cmd + m' })}
          </ThemedText>{' '}
          to open developer tools.
        </ThemedText>
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Step 2: Explore</ThemedText>
        <ThemedText>
          Tap the Explore tab to learn more about what's included in this starter app.
        </ThemedText>
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Step 3: Get a fresh start</ThemedText>
        <ThemedText>
          When you're ready, run{' '}
          <ThemedText type="defaultSemiBold">npm run reset-project</ThemedText> to get a fresh{' '}
          <ThemedText type="defaultSemiBold">app</ThemedText> directory. This will move the current{' '}
          <ThemedText type="defaultSemiBold">app</ThemedText> to{' '}
          <ThemedText type="defaultSemiBold">app-example</ThemedText>.
        </ThemedText>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
});
*/