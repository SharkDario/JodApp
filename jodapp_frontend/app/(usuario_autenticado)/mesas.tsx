import React, { useState, useRef, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Dimensions,
    FlatList,
    StatusBar,
    TouchableOpacity,
    Image,
    Modal,
    ScrollView,
    Animated,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';
import { showMessage } from "react-native-flash-message";
import {PanGestureHandler, GestureHandlerRootView } from 'react-native-gesture-handler';

const { width, height } = Dimensions.get('window');
const FLOOR_PLAN_HEIGHT = 730; //730;
const FLOOR_PLAN_WIDTH = 897; //910; // Ajustar al tamaño real del plano

const DraggableImageWithTables = ({ source, mesas, containerWidth, containerHeight, renderTable }) => {
    // Animated values for X and Y
    const translateX = useRef(new Animated.Value(0)).current;
    const translateY = useRef(new Animated.Value(0)).current;

    // Offsets to accumulate the drag distance
    const offsetX = useRef(0);
    const offsetY = useRef(0);

    const handlePanGesture = Animated.event(
        [
            {
                nativeEvent: {
                    translationX: translateX,
                    translationY: translateY,
                },
            },
        ],
        { useNativeDriver: true }
    );

    const handlePanStateChange = (event) => {
        if (event.nativeEvent.oldState === 4) { // Gesture ended
            // Accumulate the translation into offset
            offsetX.current += event.nativeEvent.translationX;
            offsetY.current += event.nativeEvent.translationY;

            // Set the final values to translateX and translateY
            translateX.setOffset(offsetX.current);
            translateY.setOffset(offsetY.current);

            // Reset the animated translation values for the next gesture
            translateX.setValue(0);
            translateY.setValue(0);
        }
    };

    return (
        <GestureHandlerRootView>
            <PanGestureHandler
                onGestureEvent={handlePanGesture}
                onHandlerStateChange={handlePanStateChange}
            >
                <Animated.View
                    style={{
                        transform: [{ translateX }, { translateY }],
                        width: containerWidth,
                        height: containerHeight,
                    }}
                >
                    {/* Plano de fondo */}
                    <Image
                        source={source}
                        style={{ width: containerWidth, height: containerHeight }}
                        resizeMode="contain"
                    />

                    {/* Mesas superpuestas */}
                    {mesas.map(renderTable)}
                </Animated.View>
            </PanGestureHandler>
        </GestureHandlerRootView>
    );
};

interface TableModalProps {
    visible: boolean;
    onClose: () => void;
    mesa: Mesa | null;
    onReserve?: () => void;
}

const TableModal = ({ visible, onClose, mesa, onReserve }: TableModalProps) => {
    if (!mesa) return null;

    const isAvailable = mesa.disponibilidad === "Disponible";

    // Doble verificación de disponibilidad
    if (!isAvailable) {
        onClose();
        return null;
    }

    return (
        <Modal
            visible={visible}
            transparent={true}
            animationType="slide"
            onRequestClose={onClose}
        >
            <View style={styles.modalOverlay}>
                <View style={styles.modalContent}>
                    <Text style={styles.modalTitle}>Mesa {mesa.numero}</Text>
                    <View style={styles.modalInfo}>
                        <Text style={styles.modalText}>Categoría: {mesa.categoria}</Text>
                        <Text style={styles.modalText}>Capacidad: {mesa.capacidad} personas</Text>
                        <Text style={styles.modalText}>Precio: ${mesa.precio}</Text>
                        <Text style={styles.modalText}>{mesa.bebidas}</Text>
                    </View>

                    {mesa.disponibilidad && (
                        <TouchableOpacity
                            style={styles.reserveButton}
                            onPress={onReserve}
                        >
                            <Text style={styles.reserveButtonText}>Reservar Mesa</Text>
                        </TouchableOpacity>
                    )}

                    <TouchableOpacity
                        style={styles.closeButton}
                        onPress={onClose}
                    >
                        <Text style={styles.closeButtonText}>Cerrar</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
};

export default function MesasScreen() {
    const { fiestas, reservarMesa } = useAuth();
    const [currentFiesta, setCurrentFiesta] = useState<Fiesta | null>(null);
    const [selectedMesa, setSelectedMesa] = useState<Mesa | null>(null);
    const [modalVisible, setModalVisible] = useState(false);
    const flatListRef = useRef<FlatList>(null);
    const [containerWidth, setContainerWidth] = useState(FLOOR_PLAN_WIDTH);
    const [containerHeight, setContainerHeight] = useState(FLOOR_PLAN_HEIGHT);

    // Combine Friday and Saturday parties
    const allFiestas = [...(fiestas?.viernes || []), ...(fiestas?.sabado || [])];

    useEffect(() => {
        const handleLayout = (event: any) => {
            const { width, height } = event.nativeEvent.layout;
            setContainerWidth(width);
            setContainerHeight(height);
        };

        return () => {
            // Limpiar event listener
        };
    }, []);

    const onScroll = (event: any) => {
        const offsetY = event.nativeEvent.contentOffset.y;
        const index = Math.floor(offsetY / (height - 80));
        setCurrentFiesta(allFiestas[index]);
    };

    const handleTablePress = (mesa: Mesa) => {
        if (mesa.disponibilidad === "Disponible") {
            setSelectedMesa(mesa);
            setModalVisible(true);
        }
    };

    const handleReserve = async () => {
        // Implementar lógica de reserva
        console.log(`Reservando mesa ${selectedMesa?.numero}`);
        if (!selectedMesa) return;
        try {
            await reservarMesa(selectedMesa?.id);
            setModalVisible(false);
        } catch (error) {
            showMessage({
                message: "Error",
                description: error instanceof Error ? error.message : "No se pudo proceder a reservar la mesa",
                type: "danger",
                duration: 3000,
                floating: true,
            });
        }
    };

    const renderTable = (mesa: Mesa) => {
        const isAvailable = mesa.disponibilidad === "Disponible";

        const tableStyle = {
            ...styles.tableMarker,
            top: (mesa.posicion.top / FLOOR_PLAN_HEIGHT) * containerHeight,
            left: (mesa.posicion.left / FLOOR_PLAN_WIDTH) * containerWidth,
            backgroundColor: mesa.disponibilidad ? mesa.color : 'red',
            borderColor: mesa.categoria === 'VIP' ? 'gold' : 'black',
            shadowColor: mesa.disponibilidad ? mesa.color : 'red',
            //opacity: isAvailable ? 1 : 0.6,
        };

        return (
            <TouchableOpacity
                key={mesa.numero}
                style={tableStyle}
                onPress={() => handleTablePress(mesa)}
                disabled={!mesa.disponibilidad}
            >
                <Text style={[
                    styles.tableNumber,
                    { color: mesa.categoria === 'VIP' ? 'gold' : 'black' }
                ]}>
                    {mesa.numero}
                </Text>
            </TouchableOpacity>
        );
    };

    const renderFiestaScreen = ({ item }: { item: Fiesta }) => {
        return (
            <View style={styles.fullScreen}>
                
                <Text style={styles.screenTitle}>{item.nombre} 🟪</Text>
                <Text style={styles.dateText}>
                    {new Date(item.fecha + 'T00:00:00').toLocaleDateString('es-ES', {
                        weekday: 'long',
                        day: '2-digit',
                        month: 'long'
                    })}
                </Text>
                <View style={styles.legend}>
                    <View style={styles.legendItem}>
                        <View style={[styles.legendDot, { backgroundColor: 'green' }]} />
                        <Text style={styles.legendText}>Disponible</Text>
                    </View>
                    <View style={styles.legendItem}>
                        <View style={[styles.legendDot, { backgroundColor: 'red' }]} />
                        <Text style={styles.legendText}>No disponible</Text>
                    </View>
                </View>
                <DraggableImageWithTables 
                    source={require('@/assets/images/plano_evento.png')}
                    mesas={item.mesas}
                    containerWidth={containerWidth}
                    containerHeight={containerHeight}
                    renderTable={renderTable}
                />
                <Text style={styles.screenTitle}></Text>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Mesas</Text>
            </View>

            <FlatList
                ref={flatListRef}
                data={allFiestas}
                renderItem={renderFiestaScreen}
                keyExtractor={(item, index) => `fiesta-${index}`}
                pagingEnabled
                snapToAlignment="start"
                decelerationRate="fast"
                snapToInterval={height - 80}
                showsVerticalScrollIndicator={false}
                onScroll={onScroll}
                scrollEventThrottle={16}
            />

            <TableModal
                visible={modalVisible}
                onClose={() => setModalVisible(false)}
                mesa={selectedMesa}
                onReserve={handleReserve}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    // Estilos existentes
    floorPlanContainer: {
        position: 'relative',
        marginBottom: 20,
    },
    floorPlanImage: {
        backgroundColor: 'white',
        borderRadius: 12,
    },
    tableMarker: {
        position: 'absolute',
        width: 40,
        height: 40,
        borderRadius: 20,
        borderWidth: 3,
        justifyContent: 'center',
        alignItems: 'center',
        shadowOffset: {
            width: 0,
            height: 0,
        },
        shadowOpacity: 0.8,
        shadowRadius: 10,
        elevation: 5,
    },
    // Otros estilos
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
        height: height - 80,
        width: width,
        padding: 20,
    },
    screenTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 8,
    },
    dateText: {
        fontSize: 16,
        color: '#B57EDC',
        marginBottom: 5,
        textTransform: 'capitalize',
    },
    tableNumber: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    legend: {
        flexDirection: 'row',
        justifyContent: 'center',
        gap: 50,
        padding: 0,
    },
    legendItem: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 2,
    },
    legendDot: {
        width: 12,
        height: 12,
        borderRadius: 6,
    },
    legendText: {
        color: 'white',
        fontSize: 14,
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 20,
        width: '80%',
        maxWidth: 400,
    },
    modalTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 16,
        textAlign: 'center',
    },
    modalInfo: {
        gap: 8,
        marginBottom: 20,
    },
    modalText: {
        fontSize: 16,
        color: '#B57EDC',
    },
    reserveButton: {
        backgroundColor: '#7C03D6',
        paddingVertical: 12,
        borderRadius: 8,
        marginBottom: 12,
    },
    reserveButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
        textAlign: 'center',
    },
    closeButton: {
        backgroundColor: '#333',
        paddingVertical: 12,
        borderRadius: 8,
    },
    closeButtonText: {
        color: 'white',
        fontSize: 16,
        textAlign: 'center',
    },
});


/* 
{/*
                <ScrollView
                    contentContainerStyle={{
                        alignItems: 'center',
                        paddingVertical: 20,
                    }}
                >


                    <View style={[
                        styles.floorPlanContainer,
                        { height: containerHeight, width: containerWidth }
                    ]}>
                        {/*
                        <Image
                            source={require('@/assets/images/plano_evento.png')}
                            style={[
                                styles.floorPlanImage,
                                { height: containerHeight, width: containerWidth }
                            ]}
                            resizeMode="contain"
                        />
                        <DraggableImage
                            source={require('@/assets/images/plano_evento.png')}
                            containerWidth={containerWidth}
                            containerHeight={containerHeight}
                            resizeMode="contain"
                        />
                        {item.mesas.map(renderTable)}
                    </View>
                    <View style={styles.legend}>
                        <View style={styles.legendItem}>
                            <View style={[styles.legendDot, { backgroundColor: 'green' }]} />
                            <Text style={styles.legendText}>Disponible</Text>
                        </View>
                        <View style={styles.legendItem}>
                            <View style={[styles.legendDot, { backgroundColor: 'red' }]} />
                            <Text style={styles.legendText}>No disponible</Text>
                        </View>
                    </View>
                </ScrollView>
                

Funciona dentro de todo
// app/(usuario_autenticado)/mesas.tsx
import React, { useState, useRef } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Dimensions,
    FlatList,
    StatusBar,
    TouchableOpacity,
    Image,
    Modal,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';

const { width, height } = Dimensions.get('window');

interface TableModalProps {
    visible: boolean;
    onClose: () => void;
    mesa: Mesa | null;
    onReserve?: () => void;
}

const TableModal = ({ visible, onClose, mesa, onReserve }: TableModalProps) => {
    if (!mesa) return null;

    return (
        <Modal
            visible={visible}
            transparent={true}
            animationType="slide"
            onRequestClose={onClose}
        >
            <View style={styles.modalOverlay}>
                <View style={styles.modalContent}>
                    <Text style={styles.modalTitle}>Mesa {mesa.numero}</Text>
                    <View style={styles.modalInfo}>
                        <Text style={styles.modalText}>Categoría: {mesa.categoria}</Text>
                        <Text style={styles.modalText}>Capacidad: {mesa.capacidad} personas</Text>
                        <Text style={styles.modalText}>Precio: ${mesa.precio}</Text>
                    </View>

                    {mesa.disponibilidad && (
                        <TouchableOpacity
                            style={styles.reserveButton}
                            onPress={onReserve}
                        >
                            <Text style={styles.reserveButtonText}>Reservar Mesa</Text>
                        </TouchableOpacity>
                    )}

                    <TouchableOpacity
                        style={styles.closeButton}
                        onPress={onClose}
                    >
                        <Text style={styles.closeButtonText}>Cerrar</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
};

export default function MesasScreen() {
    const { fiestas } = useAuth();
    const [currentFiesta, setCurrentFiesta] = useState<Fiesta | null>(null);
    const [selectedMesa, setSelectedMesa] = useState<Mesa | null>(null);
    const [modalVisible, setModalVisible] = useState(false);
    const flatListRef = useRef<FlatList>(null);

    // Combine Friday and Saturday parties
    const allFiestas = [...(fiestas?.viernes || []), ...(fiestas?.sabado || [])];

    const onScroll = (event: any) => {
        const offsetY = event.nativeEvent.contentOffset.y;
        const index = Math.floor(offsetY / (height - 80));
        setCurrentFiesta(allFiestas[index]);
    };

    const handleTablePress = (mesa: Mesa) => {
        if (mesa.disponibilidad) {
            setSelectedMesa(mesa);
            setModalVisible(true);
        }
    };

    const handleReserve = () => {
        // Implement reservation logic
        console.log(`Reservando mesa ${selectedMesa?.numero}`);
        setModalVisible(false);
    };

    const renderTable = (mesa: Mesa) => {
        const tableStyle = {
            ...styles.tableMarker,
            top: mesa.posicion.top,
            left: mesa.posicion.left,
            backgroundColor: mesa.disponibilidad ? mesa.color : 'red',
            borderColor: mesa.categoria === 'VIP' ? 'gold' : 'black',
            shadowColor: mesa.disponibilidad ? mesa.color : 'red',
        };

        return (
            <TouchableOpacity
                key={mesa.numero}
                style={tableStyle}
                onPress={() => handleTablePress(mesa)}
                disabled={!mesa.disponibilidad}
            >
                <Text style={[
                    styles.tableNumber,
                    { color: mesa.categoria === 'VIP' ? 'gold' : 'black' }
                ]}>
                    {mesa.numero}
                </Text>
            </TouchableOpacity>
        );
    };

    const renderFiestaScreen = ({ item }: { item: Fiesta }) => {
        return (
            <View style={styles.fullScreen}>
                <Text style={styles.screenTitle}>{item.nombre}</Text>
                <Text style={styles.dateText}>
                    {new Date(item.fecha + 'T00:00:00').toLocaleDateString('es-ES', {
                        weekday: 'long',
                        day: '2-digit',
                        month: 'long'
                    })}
                </Text>

                <View style={styles.floorPlanContainer}>
                    <Image
                        source={require('@/assets/images/plano_evento.png')}
                        style={styles.floorPlanImage}
                        resizeMode="contain"
                    />
                    {item.mesas.map(renderTable)}
                </View>

                <View style={styles.legend}>
                    <View style={styles.legendItem}>
                        <View style={[styles.legendDot, { backgroundColor: 'green' }]} />
                        <Text style={styles.legendText}>Disponible</Text>
                    </View>
                    <View style={styles.legendItem}>
                        <View style={[styles.legendDot, { backgroundColor: 'red' }]} />
                        <Text style={styles.legendText}>No disponible</Text>
                    </View>
                </View>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Mesas</Text>
            </View>

            <FlatList
                ref={flatListRef}
                data={allFiestas}
                renderItem={renderFiestaScreen}
                keyExtractor={(item, index) => `fiesta-${index}`}
                pagingEnabled
                snapToAlignment="start"
                decelerationRate="fast"
                snapToInterval={height - 80}
                showsVerticalScrollIndicator={false}
                onScroll={onScroll}
                scrollEventThrottle={16}
            />

            <TableModal
                visible={modalVisible}
                onClose={() => setModalVisible(false)}
                mesa={selectedMesa}
                onReserve={handleReserve}
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
        height: height - 80,
        width: width,
        padding: 20,
    },
    screenTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 8,
    },
    dateText: {
        fontSize: 16,
        color: '#B57EDC',
        marginBottom: 20,
        textTransform: 'capitalize',
    },
    floorPlanContainer: {
        flex: 1,
        position: 'relative',
        marginBottom: 20,
    },
    floorPlanImage: {
        width: '100%',
        height: '100%',
        backgroundColor: 'white',
        borderRadius: 12,
    },
    tableMarker: {
        position: 'absolute',
        width: 40,
        height: 40,
        borderRadius: 20,
        borderWidth: 3,
        justifyContent: 'center',
        alignItems: 'center',
        shadowOffset: {
            width: 0,
            height: 0,
        },
        shadowOpacity: 0.8,
        shadowRadius: 10,
        elevation: 5,
    },
    tableNumber: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    legend: {
        flexDirection: 'row',
        justifyContent: 'center',
        gap: 20,
        padding: 10,
    },
    legendItem: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    legendDot: {
        width: 12,
        height: 12,
        borderRadius: 6,
    },
    legendText: {
        color: 'white',
        fontSize: 14,
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 20,
        width: '80%',
        maxWidth: 400,
    },
    modalTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 16,
        textAlign: 'center',
    },
    modalInfo: {
        gap: 8,
        marginBottom: 20,
    },
    modalText: {
        fontSize: 16,
        color: '#B57EDC',
    },
    reserveButton: {
        backgroundColor: '#7C03D6',
        paddingVertical: 12,
        borderRadius: 8,
        marginBottom: 12,
    },
    reserveButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
        textAlign: 'center',
    },
    closeButton: {
        backgroundColor: '#333',
        paddingVertical: 12,
        borderRadius: 8,
    },
    closeButtonText: {
        color: 'white',
        fontSize: 16,
        textAlign: 'center',
    },
});





/*NOP
import React, { useState, useRef } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Dimensions,
    FlatList,
    StatusBar,
    TouchableOpacity,
    ScrollView,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';

const { width, height } = Dimensions.get('window');

export default function MesasScreen() {
    const { fiestas } = useAuth();
    const [currentFiesta, setCurrentFiesta] = useState<Fiesta | null>(null);
    const flatListRef = useRef<FlatList>(null);

    // Combine Friday and Saturday parties
    const allFiestas = [...(fiestas?.viernes || []), ...(fiestas?.sabado || [])];

    const onScroll = (event: any) => {
        const offsetY = event.nativeEvent.contentOffset.y;
        const index = Math.floor(offsetY / (height - 80));
        setCurrentFiesta(allFiestas[index]);
    };

    const renderTableMarker = (mesa: Mesa) => {
        return (
            <TouchableOpacity
                key={mesa.numero}
                style={[
                    styles.tableMarker,
                    {
                        top: mesa.posicion.top,
                        left: mesa.posicion.left,
                        backgroundColor: mesa.disponibilidad ? mesa.color : '#666',
                    },
                ]}
                onPress={() => {
                    // Implement table selection logic
                    console.log(`Mesa ${mesa.numero} seleccionada`);
                }}
            >
                <Text style={styles.tableNumber}>{mesa.numero}</Text>
            </TouchableOpacity>
        );
    };

    const renderTableInfo = (mesa: Mesa) => {
        return (
            <View key={mesa.numero} style={styles.tableInfoCard}>
                <View style={styles.tableInfoHeader}>
                    <Text style={styles.tableInfoTitle}>Mesa {mesa.numero}</Text>
                    <View
                        style={[
                            styles.statusIndicator,
                            { backgroundColor: mesa.disponibilidad ? '#4CAF50' : '#F44336' }
                        ]}
                    />
                </View>
                <View style={styles.tableInfoContent}>
                    <Text style={styles.tableInfoText}>Categoría: {mesa.categoria}</Text>
                    <Text style={styles.tableInfoText}>Capacidad: {mesa.capacidad} personas</Text>
                    <Text style={styles.tableInfoText}>Precio: $ {mesa.precio}</Text>
                    <Text style={styles.tableInfoText}>
                        Estado: {mesa.disponibilidad ? 'Disponible' : 'Reservada'}
                    </Text>
                </View>
            </View>
        );
    };

    const renderFiestaScreen = ({ item }: { item: Fiesta }) => {
        return (
            <View style={styles.fullScreen}>
                <Text style={styles.screenTitle}>{item.nombre}</Text>
                <Text style={styles.dateText}>
                    {new Date(item.fecha).toLocaleDateString('es-ES', {
                        weekday: 'long',
                        day: '2-digit',
                        month: 'long'
                    })}
                </Text>

                <View style={styles.floorPlanContainer}>
                    <Text style={styles.sectionTitle}>Plano del Local</Text>
                    <View style={styles.floorPlan}>
                        {item.mesas.map(renderTableMarker)}
                    </View>
                </View>

                <View style={styles.tableListContainer}>
                    <Text style={styles.sectionTitle}>Información de Mesas</Text>
                    <ScrollView style={styles.tableList}>
                        {item.mesas.map(renderTableInfo)}
                    </ScrollView>
                </View>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Mesas</Text>
            </View>

            <FlatList
                ref={flatListRef}
                data={allFiestas}
                renderItem={renderFiestaScreen}
                keyExtractor={(item, index) => `fiesta-${index}`}
                pagingEnabled
                snapToAlignment="start"
                decelerationRate="fast"
                snapToInterval={height - 80}
                showsVerticalScrollIndicator={false}
                onScroll={onScroll}
                scrollEventThrottle={16}
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
        height: height - 80,
        width: width,
        padding: 20,
    },
    screenTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 8,
    },
    dateText: {
        fontSize: 16,
        color: '#B57EDC',
        marginBottom: 20,
        textTransform: 'capitalize',
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 16,
    },
    floorPlanContainer: {
        marginBottom: 20,
    },
    floorPlan: {
        height: 200,
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        position: 'relative',
    },
    tableMarker: {
        position: 'absolute',
        width: 40,
        height: 40,
        borderRadius: 20,
        justifyContent: 'center',
        alignItems: 'center',
    },
    tableNumber: {
        color: 'white',
        fontWeight: 'bold',
    },
    tableListContainer: {
        flex: 1,
    },
    tableList: {
        flex: 1,
    },
    tableInfoCard: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 16,
        marginBottom: 12,
    },
    tableInfoHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12,
    },
    tableInfoTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: 'white',
    },
    statusIndicator: {
        width: 12,
        height: 12,
        borderRadius: 6,
    },
    tableInfoContent: {
        gap: 8,
    },
    tableInfoText: {
        fontSize: 16,
        color: '#B57EDC',
    },
});
*/