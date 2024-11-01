import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Dimensions, Image, TouchableWithoutFeedback, Platform } from 'react-native';
import Animated, { interpolate, useAnimatedStyle, useSharedValue, withSpring, withRepeat, withTiming, Easing } from 'react-native-reanimated';
import Carousel from 'react-native-reanimated-carousel';
import { BlurView } from 'expo-blur';

const { width } = Dimensions.get('window');

// Datos del carrusel con URLs de imágenes y textos para ambos lados de la tarjeta
// Image mapping
const imageMapping = {
  'jodapp-logo': require('@/assets/images/jodapp-logo.png'),
  'azul_roxo': require('@/assets/images/azul_roxo.jpg'),
  'bebidas_1': require('@/assets/images/bebidas_1.jpg'),
  'club_1': require('@/assets/images/club_1.jpg'),
  'club_2': require('@/assets/images/club_2.jpeg'),
  'club_3': require('@/assets/images/club_3.webp'),
  'mesa_1': require('@/assets/images/mesa_1.jpg'),
};

interface HoverCardProps {
    title: string;
    frontText: string;
    backText: string;
    image: string;
}

function HoverCard({ frontText, backText, image }: HoverCardProps) {
  const flipValue = useSharedValue(0);

  const frontAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          rotateY: `${interpolate(flipValue.value, [0, 1], [0, 180])}deg`,
        },
      ],
      opacity: interpolate(flipValue.value, [0, 0.5, 0.5, 1], [1, 1, 0, 0]),
    };
  });

  const backAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          rotateY: `${interpolate(flipValue.value, [0, 1], [180, 360])}deg`,
        },
      ],
      opacity: interpolate(flipValue.value, [0, 0.5, 0.5, 1], [0, 0, 1, 1]),
    };
  });

  const handlePress = () => {
    flipValue.value = withSpring(flipValue.value === 0 ? 1 : 0);
  };

  return (
    <TouchableWithoutFeedback onPress={handlePress}>
      <View style={styles.cardContainer}>
        <Animated.View style={[styles.card, frontAnimatedStyle]}>
          <Image source={imageMapping[image]} style={styles.cardImage} />
          <Text style={styles.cardText}>{frontText}</Text>
        </Animated.View>
        <Animated.View style={[styles.card, styles.backCard, backAnimatedStyle]}>
          <Image source={imageMapping[image]} style={styles.cardImage} />
          {Platform.OS !== 'web' && <BlurView intensity={80} style={styles.absolute} />}
          <View style={[styles.absolute, { backgroundColor: 'rgba(71, 38, 118, 0.7)' }]} />
          <Text style={styles.cardText}>{backText}</Text>
        </Animated.View>
      </View>
    </TouchableWithoutFeedback>
  );
}

interface ParallaxCarouselProps {
    data_arg: HoverCardProps[];
}

export default function ParallaxCarousel({ data_arg }: ParallaxCarouselProps) {
  const carouselRef = useRef(null);
  const autoPlayProgress = useSharedValue(0);

  useEffect(() => {
    autoPlayProgress.value = withRepeat(
      withTiming(1, { duration: 3000, easing: Easing.linear }),
      -1,
      false
    );
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (carouselRef.current) {
        carouselRef.current.next();
      }
    }, 3000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <Carousel
      ref={carouselRef}
      width={width}
      height={340}
      data={data_arg}
      renderItem={({ item, index, animationValue }) => {
        const animatedStyle = useAnimatedStyle(() => {
          const translateX = interpolate(
            animationValue.value,
            [-1, 0, 1],
            [-width * 0.5, 0, width * 0.5]
          );

          return {
            transform: [{ translateX }],
          };
        });

        return (
          <Animated.View style={[styles.itemContainer, animatedStyle]}>
            <HoverCard
              frontText={item.frontText}
              backText={item.backText}
              image={item.image}
            />
            <Text style={styles.title}>{item.title}</Text>
          </Animated.View>
        );
      }}
      autoPlay={Platform.OS !== 'web'}
      autoPlayInterval={7000}
      scrollAnimationDuration={2000}
    />
  );
}

const styles = StyleSheet.create({
  itemContainer: {
    width,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 0,
  },
  cardContainer: {
    width: width * 0.8,
    height: 300,
    padding: 0,
  },
  card: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    backfaceVisibility: 'hidden',
    overflow: 'hidden',
  },
  backCard: {
    backgroundColor: 'transparent',
  },
  cardImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  cardText: {
    position: 'absolute',
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 10,
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  title: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  absolute: {
    position: "absolute",
    top: 0,
    left: 0,
    bottom: 0,
    right: 0,
  },
});
/*
//Version 2.0
import React from 'react';
import { View, Text, StyleSheet, Dimensions, Image, TouchableWithoutFeedback } from 'react-native';
import Animated, { interpolate, useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';
import Carousel from 'react-native-reanimated-carousel';
import { BlurView } from 'expo-blur';

const { width } = Dimensions.get('window');

// Datos del carrusel con URLs de imágenes y textos para ambos lados de la tarjeta
const data = [
  {
    title: 'Capa 1',
    image: 'https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA',
    frontText: 'Frente de la Tarjeta 1',
    backText: 'Reverso de la Tarjeta 1',
  },
  {
    title: 'Capa 2',
    image: 'https://fastly.picsum.photos/id/29/4000/2670.jpg?hmac=rCbRAl24FzrSzwlR5tL-Aqzyu5tX_PA95VJtnUXegGU',
    frontText: 'Frente de la Tarjeta 2',
    backText: 'Reverso de la Tarjeta 2',
  },
  {
    title: 'Capa 3',
    image: 'https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA',
    frontText: 'Frente de la Tarjeta 3',
    backText: 'Reverso de la Tarjeta 3',
  },
];

// Definir la interfaz para las propiedades del componente
interface HoverCardProps {
    frontText: string; // Texto que se muestra inicialmente
    backText: string;  // Texto que se muestra cuando se voltea
    image: string;
}

function HoverCard({ frontText, backText, image }: HoverCardProps) {
  const flipValue = useSharedValue(0);

  const frontAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          rotateY: `${interpolate(flipValue.value, [0, 1], [0, 180])}deg`,
        },
      ],
      opacity: interpolate(flipValue.value, [0, 0.5, 0.5, 1], [1, 1, 0, 0]),
    };
  });

  const backAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          rotateY: `${interpolate(flipValue.value, [0, 1], [180, 360])}deg`,
        },
      ],
      opacity: interpolate(flipValue.value, [0, 0.5, 0.5, 1], [0, 0, 1, 1]),
    };
  });

  const handlePress = () => {
    flipValue.value = withSpring(flipValue.value === 0 ? 1 : 0);
  };

  return (
    <TouchableWithoutFeedback onPress={handlePress}>
      <View style={styles.cardContainer}>
        <Animated.View style={[styles.card, frontAnimatedStyle]}>
          <Image source={{ uri: image }} style={styles.cardImage} />
          <Text style={styles.cardText}>{frontText}</Text>
        </Animated.View>
        <Animated.View style={[styles.card, styles.backCard, backAnimatedStyle]}>
          <Image source={{ uri: image }} style={styles.cardImage} />
          <BlurView intensity={80} style={styles.absolute} />
          <Text style={styles.cardText}>{backText}</Text>
        </Animated.View>
      </View>
    </TouchableWithoutFeedback>
  );
}

export default function ParallaxCarousel() {
  return (
    <Carousel
      width={width}
      height={400}
      data={data}
      renderItem={({ item, index, animationValue }) => {
        const animatedStyle = useAnimatedStyle(() => {
          const translateX = interpolate(
            animationValue.value,
            [-1, 0, 1],
            [-width * 0.5, 0, width * 0.5]
          );

          return {
            transform: [{ translateX }],
          };
        });

        return (
          <Animated.View style={[styles.itemContainer, animatedStyle]}>
            <HoverCard
              frontText={item.frontText}
              backText={item.backText}
              image={item.image}
            />
            <Text style={styles.title}>{item.title}</Text>
          </Animated.View>
        );
      }}
    />
  );
}

const styles = StyleSheet.create({
  itemContainer: {
    width,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardContainer: {
    width: width * 0.8,
    height: 300,
  },
  card: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    backfaceVisibility: 'hidden',
    overflow: 'hidden',
  },
  backCard: {
    backgroundColor: 'transparent',
  },
  cardImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  cardText: {
    position: 'absolute',
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 10,
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  title: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  absolute: {
    position: "absolute",
    top: 0,
    left: 0,
    bottom: 0,
    right: 0,
  },
});

/*
import React, { useState } from 'react';
import { View, Text, StyleSheet, Dimensions, Image, TouchableWithoutFeedback } from 'react-native';
import Animated, { interpolate, useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';
import Carousel from 'react-native-reanimated-carousel';

const { width } = Dimensions.get('window');

// Datos del carrusel con URLs de imágenes y textos para ambos lados de la tarjeta
const data = [
  {
    title: 'Capa 1',
    image: 'https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA',
    frontText: 'Frente de la Tarjeta 1',
    backText: 'Reverso de la Tarjeta 1',
  },
  {
    title: 'Capa 2',
    image: 'https://fastly.picsum.photos/id/29/4000/2670.jpg?hmac=rCbRAl24FzrSzwlR5tL-Aqzyu5tX_PA95VJtnUXegGU',
    frontText: 'Frente de la Tarjeta 2',
    backText: 'Reverso de la Tarjeta 2',
  },
  {
    title: 'Capa 3',
    image: 'https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA',
    frontText: 'Frente de la Tarjeta 3',
    backText: 'Reverso de la Tarjeta 3',
  },
];

// Definir la interfaz para las propiedades del componente
interface HoverCardProps {
    frontText: string; // Texto que se muestra inicialmente
    backText: string;  // Texto que se muestra cuando se voltea
    image: string;
}

function HoverCard({ frontText, backText, image }: HoverCardProps) {
  const flipValue = useSharedValue(0);

  const frontAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          rotateY: `${interpolate(flipValue.value, [0, 1], [0, 180])}deg`,
        },
      ],
      opacity: interpolate(flipValue.value, [0, 0.5, 0.5, 1], [1, 1, 0, 0]),
    };
  });

  const backAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          rotateY: `${interpolate(flipValue.value, [0, 1], [180, 360])}deg`,
        },
      ],
      opacity: interpolate(flipValue.value, [0, 0.5, 0.5, 1], [0, 0, 1, 1]),
    };
  });

  const handlePress = () => {
    flipValue.value = withSpring(flipValue.value === 0 ? 1 : 0);
  };

  return (
    <TouchableWithoutFeedback onPress={handlePress}>
      <View style={styles.cardContainer}>
        <Animated.View style={[styles.card, frontAnimatedStyle]}>
          <Image source={{ uri: image }} style={styles.cardImage} />
          <Text style={styles.cardText}>{frontText}</Text>
        </Animated.View>
        <Animated.View style={[styles.card, styles.backCard, backAnimatedStyle]}>
          <Text style={styles.cardText}>{backText}</Text>
        </Animated.View>
      </View>
    </TouchableWithoutFeedback>
  );
}

export default function ParallaxCarousel() {
  return (
    <Carousel
      width={width}
      height={400}
      data={data}
      renderItem={({ item, index, animationValue }) => {
        const animatedStyle = useAnimatedStyle(() => {
          const translateX = interpolate(
            animationValue.value,
            [-1, 0, 1],
            [-width * 0.5, 0, width * 0.5]
          );

          return {
            transform: [{ translateX }],
          };
        });

        return (
          <Animated.View style={[styles.itemContainer, animatedStyle]}>
            <HoverCard
              frontText={item.frontText}
              backText={item.backText}
              image={item.image}
            />
            <Text style={styles.title}>{item.title}</Text>
          </Animated.View>
        );
      }}
    />
  );
}

const styles = StyleSheet.create({
  itemContainer: {
    width,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardContainer: {
    width: width * 0.8,
    height: 300,
  },
  card: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    backfaceVisibility: 'hidden',
    overflow: 'hidden',
  },
  backCard: {
    backgroundColor: '#555',
  },
  cardImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  cardText: {
    position: 'absolute',
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 10,
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  title: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
});

/* Otro
import React from 'react';
import { View, Text, StyleSheet, Dimensions, Image } from 'react-native';
import Animated, { interpolate, useAnimatedStyle } from 'react-native-reanimated';
import Carousel from 'react-native-reanimated-carousel';

const { width } = Dimensions.get('window');

// Datos del carrusel con URLs de imágenes de placeholder
const data = [
    {
      title: 'Capa 1',
      image: 'https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA',
    },
    {
      title: 'Capa 2',
      image: 'https://fastly.picsum.photos/id/29/4000/2670.jpg?hmac=rCbRAl24FzrSzwlR5tL-Aqzyu5tX_PA95VJtnUXegGU',
    },
    {
      title: 'Capa 3',
      image: 'https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA',
    },
];

export default function ParallaxCarousel() {
  return (
    <Carousel
      width={width}
      height={400}
      data={data}
      renderItem={({ item, index, animationValue }) => {
        const animatedStyle = useAnimatedStyle(() => {
          const translateX = interpolate(
            animationValue.value,
            [-1, 0, 1],
            [-width * 0.5, 0, width * 0.5]
          );

          return {
            transform: [{ translateX }],
          };
        });

        return (
          <View style={styles.itemContainer}>
            <Animated.View style={[styles.imageContainer, animatedStyle]}>
              <Image source={{ uri: item.image }} style={styles.image} />
            </Animated.View>
            <Text style={styles.title}>{item.title}</Text>
          </View>
        );
      }}
    />
  );
}

const styles = StyleSheet.create({
  itemContainer: {
    width,
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageContainer: {
    width: width * 0.8,
    height: 200,
    overflow: 'hidden',
    borderRadius: 10,
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  title: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
});*/