import React, { useState } from 'react';
import { View, Text, StyleSheet, Animated, TouchableWithoutFeedback } from 'react-native';

// Definir la interfaz para las propiedades del componente
interface HoverCardProps {
  frontText: string; // Texto que se muestra inicialmente
  backText: string;  // Texto que se muestra cuando se voltea
}

export default function HoverCard({ frontText, backText }: HoverCardProps) {
  const [flipValue] = useState(new Animated.Value(0));
  const [isFlipped, setIsFlipped] = useState(false);

  // Interpolación para el giro de la tarjeta (frente)
  const frontAnimatedStyle = {
    transform: [
      {
        rotateY: flipValue.interpolate({
          inputRange: [0, 1],
          outputRange: ['0deg', '180deg'],
        }),
      },
    ],
  };

  // Interpolación para el giro de la tarjeta (parte trasera)
  const backAnimatedStyle = {
    transform: [
      {
        rotateY: flipValue.interpolate({
          inputRange: [0, 1],
          outputRange: ['180deg', '360deg'],
        }),
      },
    ],
  };

  // Interpolación para la visibilidad
  const frontOpacity = flipValue.interpolate({
    inputRange: [0, 0.5, 0.5, 1],
    outputRange: [1, 1, 0, 0],
  });

  const backOpacity = flipValue.interpolate({
    inputRange: [0, 0.5, 0.5, 1],
    outputRange: [0, 0, 1, 1],
  });

  const handlePress = () => {
    // Animación de giro
    Animated.spring(flipValue, {
      toValue: isFlipped ? 0 : 1,
      friction: 5,
      useNativeDriver: true,
    }).start(() => {
      setIsFlipped(!isFlipped);
    });
  };

  return (
    <TouchableWithoutFeedback onPress={handlePress}>
      <View style={styles.container}>
        {/* Tarjeta frontal */}
        <Animated.View style={[styles.card, frontAnimatedStyle, { opacity: frontOpacity }]}>
          <Text style={styles.cardText}>{frontText}</Text>
        </Animated.View>
        {/* Tarjeta trasera */}
        <Animated.View style={[styles.card, styles.backCard, backAnimatedStyle, { opacity: backOpacity }]}>
          <Text style={styles.cardText}>{backText}</Text>
        </Animated.View>
      </View>
    </TouchableWithoutFeedback>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 250,
    height: 250,
  },
  card: {
    position: 'absolute',
    width: 250,
    height: 250,
    backgroundColor: '#333',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    backfaceVisibility: 'hidden',
  },
  backCard: {
    backgroundColor: '#555', // Diferente color para la parte trasera
  },
  cardText: {
    color: '#fff',
    fontSize: 16,
  },
});
