
// app/(usuario_autenticado)/index.tsx
import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Dimensions,
    Image,
    TouchableOpacity,
    FlatList,
    StatusBar,
} from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { useAuth } from '@/context/AuthContext';

const { width, height } = Dimensions.get('window');

export default function DashboardScreen() {
    const { user, fiestas } = useAuth();
    const [activeMap, setActiveMap] = useState<string | null>(null);

    // Create a mapping for the images
    const imageMap = {
        1: require('@/assets/images/fiesta_1.jpg'),
        2: require('@/assets/images/fiesta_2.jpg'),
        3: require('@/assets/images/fiesta_3.jpg'),
        4: require('@/assets/images/fiesta_4.jpg'),
        5: require('@/assets/images/fiesta_5.jpg'),
        6: require('@/assets/images/fiesta_6.jpg'),
    };

    // Start the image index at 1
    let currentImageIndex = 1;

    // Generate screens for Friday's fiestas
    const fridayScreens = fiestas?.viernes.map((fiesta, index) => {
        const screen = {
            id: `viernes-${index + 1}`,
            title: `Next Viernes 🌙 ${fiesta.nombre}`,
            image: imageMap[currentImageIndex] || imageMap[1], // Use the current image or a fallback
            location: {
                latitude: fiesta.latitud,
                longitude: fiesta.longitud,
            },
            details: fiesta,
        };
        currentImageIndex++; // Increment image index for the next screen
        return screen;
    }) || [];

    // Generate screens for Saturday's fiestas
    const saturdayScreens = fiestas?.sabado.map((fiesta, index) => {
        const screen = {
            id: `sabado-${index + 1}`,
            title: `Next Sábado 🌕 ${fiesta.nombre}`,
            image: imageMap[currentImageIndex] || imageMap[1], // Use the current image or a fallback
            location: {
                latitude: fiesta.latitud,
                longitude: fiesta.longitud,
            },
            details: fiesta,
        };
        currentImageIndex++; // Increment image index for the next screen
        return screen;
    }) || [];

    // Combine Friday and Saturday screens
    const screens = [
        ...fridayScreens,
        ...saturdayScreens,
    ];

    // Insert the "Domingo" screen at the third position
    screens.splice(2, 0, {
        id: '3',
        title: 'Domingo',
        stats: true,
    });


    const renderScreen = ({ item }) => {
        if (item.stats) {
            return (
                <View style={styles.fullScreen}>
                    <View style={styles.fullScreen_2}>
                    <Text style={styles.screenTitle}>STATS</Text>
                    <View style={styles.statsContainer}>
                        <View style={styles.ticketsContainer}>
                            <View style={styles.ticketCard}>
                                <View style={styles.ticketHeader}>
                                    <Text style={styles.ticketType}>Racha</Text>
                                    <Text style={styles.ticketAmount}></Text>
                                </View>
                                <View style={styles.ticketBody}>
                                    <Text style={styles.ticketPrice}>0 🔥</Text>
                                    
                                </View>
                            </View>
                        </View>
                    </View>

                    <View style={styles.statsContainer}>
                        <View style={styles.ticketsContainer}>
                            <View style={styles.ticketCard}>
                                <View style={styles.ticketHeader}>
                                    <Text style={styles.ticketType}>Mesas Reservadas</Text>
                                    <Text style={styles.ticketAmount}></Text>
                                </View>
                                <View style={styles.ticketBody}>
                                        <Text style={styles.ticketPrice}>0 🟪</Text>

                                </View>
                            </View>
                        </View>
                    </View>

                    <View style={styles.statsContainer}>
                        <View style={styles.ticketsContainer}>
                            <View style={styles.ticketCard}>
                                <View style={styles.ticketHeader}>
                                    <Text style={styles.ticketType}>Entradas Compradas</Text>
                                    <Text style={styles.ticketAmount}></Text>
                                </View>
                                <View style={styles.ticketBody}>
                                        <Text style={styles.ticketPrice}>0 🎟️</Text>

                                </View>
                            </View>
                        </View>
                    </View>

                    <View style={styles.statsContainer}>
                        <View style={styles.ticketsContainer}>
                            <View style={styles.ticketCard}>
                                <View style={styles.ticketHeader}>
                                    <Text style={styles.ticketType}>Bebidas Compradas</Text>
                                    <Text style={styles.ticketAmount}></Text>
                                </View>
                                <View style={styles.ticketBody}>
                                        <Text style={styles.ticketPrice}>0 🍸</Text>

                                </View>
                            </View>
                        </View>
                    </View>
                    </View>
                </View>
            );
        }

        const formattedDate = new Date(item.details.fecha + 'T00:00:00').toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit'
        });

        return (
            <View style={styles.fullScreen}>
                <Text style={styles.screenTitle}>{item.title} <Text style={styles.smallText}>({formattedDate})</Text></Text>

                <View style={styles.imageContainer}>
                    <Image source={item.image} style={styles.fullImage} />
                    <TouchableOpacity
                        style={styles.locationButton}
                        onPress={() => setActiveMap(activeMap === item.id ? null : item.id)}
                    >
                        <Text style={styles.locationButtonText}>Ver ubicación 📍</Text>
                    </TouchableOpacity>

                    {activeMap === item.id && (
                        <View style={styles.mapContainer}>
                            <MapView
                                style={styles.map}
                                initialRegion={{
                                    latitude: item.location.latitude,
                                    longitude: item.location.longitude,
                                    latitudeDelta: 0.0922,
                                    longitudeDelta: 0.0421,
                                }}
                                showsUserLocation={true}
                            >
                                <Marker
                                    coordinate={item.location}
                                    title={item.details.nombre}
                                    description={formattedDate}
                                />
                            </MapView>
                        </View>
                    )}
                </View>

                <Text style={styles.statTitle}>{item.details.categoria} ✨  {item.details.vestimenta} 👗  {item.details.descripcion} 🎵</Text>
                <Text style={styles.statTitle}>Ingreso: de {item.details.edad_minima} años a {item.details.edad_maxima} años.</Text>
                <Text style={styles.statFinal}>Popular: {item.details.cantidad_entrada_popular} 🎟️ VIP: {item.details.cantidad_entrada_vip} 🎟️</Text>
                <Text></Text>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>JodApp</Text>
            </View>

            <FlatList
                data={screens}
                renderItem={renderScreen}
                keyExtractor={(item) => item.id}
                pagingEnabled
                snapToAlignment="start"
                decelerationRate="fast"
                snapToInterval={height - 80} // Subtract header height
                showsVerticalScrollIndicator={false}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'black',
    },
    header: {
        height: 80,
        backgroundColor: '#7C03D6',
        justifyContent: 'flex-end',
        paddingBottom: 10,
        paddingHorizontal: 20,
    },
    headerTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
    },
    fullScreen: {
        height: height - 80, // Subtract header height
        width: width,
    },
    fullScreen_2: {
        height: height-200, // Subtract header height
        width: width,
    },
    screenTitle: {
        fontSize: 18,
        color: 'white',
        padding: 10,
        fontWeight: 'bold',
    },
    smallText: {
        fontSize: 14,  // Tamaño más pequeño para la fecha
        color: 'white',
    },
    imageContainer: {
        flex: 1,
        position: 'relative',
    },
    fullImage: {
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    },
    locationButton: {
        position: 'absolute',
        top: 20,
        right: 20,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        paddingHorizontal: 15,
        paddingVertical: 8,
        borderRadius: 20,
    },
    locationButtonText: {
        color: 'white',
        fontSize: 16,
    },
    mapContainer: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 200,
    },
    map: {
        width: '100%',
        height: '100%',
    },
    statsContainer: {
        flex: 1,
        flexDirection: 'row',
        padding: 16,
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    statCard: {
        flex: 1,
        backgroundColor: '#B57EDC',
        padding: 16,
        borderRadius: 8,
        margin: 4,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    statTitle: {
        fontSize: 14,
        color: 'white',
        //marginTop: 10,
        //marginBottom: 8,
    },
    statFinal: {
        fontSize: 14,
        color: 'white',
        //marginTop: 10,
        marginBottom: 50,
    },
    statValue: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#7C03D6',
    },
    ticketsContainer: {
        flex: 1,
    },
    ticketsList: {
        gap: 16,
    },
    ticketCard: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 16,
        marginBottom: 20,
    },
    ticketHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12,
    },
    ticketType: {
        fontSize: 20,
        fontWeight: 'bold',
        color: 'white',
    },
    ticketAmount: {
        fontSize: 16,
        color: '#B57EDC',
    },
    ticketBody: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    ticketPrice: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#7C03D6',
    },
});