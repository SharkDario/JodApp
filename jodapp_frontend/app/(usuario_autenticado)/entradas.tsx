import React, { useState, useRef, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Dimensions,
    FlatList,
    StatusBar,
    TouchableOpacity,
    Modal,
    TextInput,
} from 'react-native';
import { showMessage } from "react-native-flash-message";
import { useAuth } from '@/context/AuthContext';

const { width, height } = Dimensions.get('window');

interface QuantityModalProps {
    visible: boolean;
    onClose: () => void;
    onConfirm: (cantidad: number) => void;
    maxQuantity: number;
}

const QuantityModal: React.FC<QuantityModalProps> = ({ visible, onClose, onConfirm, maxQuantity }) => {
    const [quantity, setQuantity] = useState('1');

    return (
        <Modal
            visible={visible}
            transparent
            animationType="slide"
        >
            <View style={styles.modalOverlay}>
                <View style={styles.modalContent}>
                    <Text style={styles.modalTitle}>Seleccionar cantidad</Text>
                    <TextInput
                        style={styles.quantityInput}
                        keyboardType="number-pad"
                        value={quantity}
                        onChangeText={(text) => setQuantity(text)}
                        maxLength={2}
                    />
                    <Text style={styles.availableText}>Disponibles: {maxQuantity}</Text>
                    <View style={styles.modalButtons}>
                        <TouchableOpacity style={styles.cancelButton} onPress={onClose}>
                            <Text style={styles.buttonText}>Cancelar</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={styles.confirmButton}
                            onPress={() => {
                                const qty = parseInt(quantity);
                                if (qty > 0 && qty <= maxQuantity) {
                                    onConfirm(qty);
                                    onClose();
                                } else {
                                    showMessage({
                                        message: "Error",
                                        description: "Cantidad inválida",
                                        type: "danger",
                                        duration: 3000,
                                        floating: true,
                                    });
                                }
                            }}
                        >
                            <Text style={styles.buttonText}>Confirmar</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </Modal>
    );
};

export default function EntradasScreen() {
    const { fiestas, cliente, comprarEntradas } = useAuth();
    const [currentFiesta, setCurrentFiesta] = useState<Fiesta | null>(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [selectedTicket, setSelectedTicket] = useState<Entrada | null>(null);
    const flatListRef = useRef<FlatList>(null);

    // Combine Friday and Saturday parties
    const allFiestas = [...(fiestas?.viernes || []), ...(fiestas?.sabado || [])];

    useEffect(() => {
        if (allFiestas.length > 0 && !currentFiesta) {
            setCurrentFiesta(allFiestas[0]);
        }
    }, [allFiestas]);

    const onScroll = (event: any) => {
        const offsetY = event.nativeEvent.contentOffset.y;
        const index = Math.floor(offsetY / (height - 80));
        if (index >= 0 && index < allFiestas.length) {
            setCurrentFiesta(allFiestas[index]);
        }
    };

    const handleBuyTicket = (entrada: Entrada) => {
        setSelectedTicket(entrada);
        setModalVisible(true);
    };

    const renderTicketCard = ({ item }: { item: Entrada }) => {
        const cantidad = item.categoria.toLowerCase() === 'vip'
            ? currentFiesta?.cantidad_entrada_vip
            : currentFiesta?.cantidad_entrada_popular;

        return (
            <View style={styles.ticketCard}>
                <View style={styles.ticketHeader}>
                    <Text style={styles.ticketType}>{item.categoria}</Text>
                    <Text style={styles.ticketAmount}>Disponibles: {cantidad}</Text>
                </View>
                <View style={styles.ticketBody}>
                    <Text style={styles.ticketPrice}>$ {item.precio_unitario}</Text>
                    <TouchableOpacity
                        style={styles.buyButton}
                        onPress={() => handleBuyTicket(item)}
                        //onPress={() => {
                        //    // Implement purchase logic
                        //    console.log(`Comprar entrada ${item.categoria}`);
                        //}}
                    >
                        <Text style={styles.buyButtonText}>Comprar</Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    };

    const renderFiestaScreen = ({ item }: { item: Fiesta }) => {
        return (
            <View style={styles.fullScreen}>
                <Text style={styles.screenTitle}>{item.nombre} 🎟️</Text>
                <Text style={styles.dateText}>
                    {new Date(item.fecha + 'T00:00:00').toLocaleDateString('es-ES', {
                        weekday: 'long',
                        day: '2-digit',
                        month: 'long'
                    })}
                </Text>

                <View style={styles.ticketsContainer}>
                    <FlatList
                        data={item.entradas}
                        renderItem={renderTicketCard}
                        keyExtractor={(ticket, index) => `${ticket.categoria}-${index}`}
                        contentContainerStyle={styles.ticketsList}
                    />
                </View>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Entradas</Text>
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
            <QuantityModal
                visible={modalVisible}
                onClose={() => setModalVisible(false)}
                onConfirm={(cantidad) => {
                    if (selectedTicket && currentFiesta) {
                        comprarEntradas(selectedTicket.id, cantidad, currentFiesta.id);
                    }
                }}
                maxQuantity={
                    selectedTicket?.categoria.toLowerCase() === 'vip'
                        ? currentFiesta?.cantidad_entrada_vip || 0
                        : currentFiesta?.cantidad_entrada_popular || 0
                }
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
        marginBottom: 16,
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
    buyButton: {
        backgroundColor: '#7C03D6',
        paddingHorizontal: 24,
        paddingVertical: 12,
        borderRadius: 8,
    },
    buyButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        backgroundColor: '#1a1a1a',
        padding: 20,
        borderRadius: 15,
        width: '80%',
    },
    modalTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: 20,
        textAlign: 'center',
    },
    quantityInput: {
        backgroundColor: '#2a2a2a',
        color: '#ffffff',
        padding: 10,
        borderRadius: 10,
        fontSize: 18,
        textAlign: 'center',
        marginBottom: 10,
    },
    availableText: {
        color: '#cccccc',
        textAlign: 'center',
        marginBottom: 20,
    },
    modalButtons: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        gap: 10,
    },
    cancelButton: {
        flex: 1,
        backgroundColor: '#444444',
        padding: 15,
        borderRadius: 10,
        alignItems: 'center',
    },
    confirmButton: {
        flex: 1,
        backgroundColor: '#007AFF',
        padding: 15,
        borderRadius: 10,
        alignItems: 'center',
    },
    buttonText: {
        color: '#ffffff',
        fontSize: 16,
        fontWeight: 'bold',
    },
});
