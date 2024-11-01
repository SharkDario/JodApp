import React, { useState, useEffect, ActivityIndicator } from 'react';
import {
    View,
    Text,
    ScrollView,
    Image,
    StyleSheet,
    Dimensions,
    TouchableOpacity,
    TextInput,
    StatusBar,
    SafeAreaView,
    Alert,
} from 'react-native';
import { showMessage } from "react-native-flash-message";
import { useAuth } from '@/context/AuthContext';
import ImageWithSearch from '@/components/ImageWithSearch';

const { width, height } = Dimensions.get('window');

interface CartItem {
    id: number;
    nombre: string;
    cantidad: number;
    precio_unitario: number;
    tipo: 'trago' | 'producto';
    detalle: string; // Para guardar el tipo de trago o marca del producto
    volumen: number;
}

const BarScreen = () => {
    const { tragos, productos, comprarCarrito } = useAuth();
    const [cart, setCart] = useState<CartItem[]>([]);
    const [quantities, setQuantities] = useState<{ [key: string]: string }>({});
    const [totalAmount, setTotalAmount] = useState(0);
    const [errors, setErrors] = useState<{ [key: string]: string }>({});

    useEffect(() => {
        const newTotal = cart.reduce((acc, item) => {
            return acc + (item.precio_unitario * item.cantidad);
        }, 0);
        setTotalAmount(newTotal);
    }, [cart]);

    const validateStock = (item: Trago | Producto, quantity: number, tipo: 'trago' | 'producto') => {
        // Verificar cantidad en el carrito actual
        const cartItem = cart.find(i => i.id === item.id && i.tipo === tipo);
        const currentCartQuantity = cartItem ? cartItem.cantidad : 0;
        const totalRequested = currentCartQuantity + quantity;

        if (totalRequested > item.stock) {
            setErrors({
                ...errors,
                [item.nombre]: `Stock insuficiente. Disponible: ${item.stock - currentCartQuantity}`
            });
            return false;
        }

        setErrors({
            ...errors,
            [item.nombre]: ''
        });
        return true;
    };

    const handleAddToCart = (item: Trago | Producto, tipo: 'trago' | 'producto') => {
        const quantity = parseInt(quantities[item.nombre] || '0');
        if (quantity <= 0) {
            setErrors({
                ...errors,
                [item.nombre]: 'La cantidad debe ser mayor a 0'
            });
            return;
        }

        if (!validateStock(item, quantity, tipo)) {
            return;
        }

        const existingItem = cart.find(cartItem => cartItem.id === item.id && cartItem.tipo === tipo);
        if (existingItem) {
            setCart(cart.map(cartItem =>
                cartItem.id === item.id && cartItem.tipo === tipo
                    ? { ...cartItem, cantidad: cartItem.cantidad + quantity }
                    : cartItem
            ));
        } else {
            setCart([...cart, {
                id: item.id,
                nombre: item.nombre,
                cantidad: quantity,
                precio_unitario: item.precio_unitario,
                tipo,
                detalle: tipo === 'trago' ? (item as Trago).tipo : (item as Producto).marca,
                volumen: item.volumen,
            }]);
        }
        setQuantities({ ...quantities, [item.nombre]: '' });
        setErrors({ ...errors, [item.nombre]: '' });
    };

    const handleRemoveFromCart = (itemId: number, tipo: 'trago' | 'producto') => {
        setCart(cart.filter(item => !(item.id === itemId && item.tipo === tipo)));
    };

    const handlePurchase = async () => {
        // Validar stock final antes de la compra
        const stockValidation = cart.every(cartItem => {
            const sourceItem = cartItem.tipo === 'trago'
                ? tragos.find(t => t.id === cartItem.id)
                : productos.find(p => p.id === cartItem.id);

            return sourceItem && cartItem.cantidad <= sourceItem.stock;
        });

        if (!stockValidation) {
            showMessage({
                message: "Error",
                description: "Algunos productos ya no tienen stock suficiente. Por favor revisa tu 🛒.",
                type: "danger",
                duration: 3000,
                floating: true,
            });
            return;
        }

        const purchaseData = {
            items: cart.map(item => ({
                id: item.id,
                tipo: item.tipo,
                cantidad: item.cantidad,
            })),
            total: totalAmount,
        };

        try {
            console.log('Iniciando compra:', purchaseData);
            const response = await comprarCarrito(purchaseData);

            // Solo resetear el carrito si la compra fue exitosa
            if (response.success) {
                setCart([]);
                setQuantities({});
                setErrors({});

                showMessage({
                    message: "¡Éxito!",
                    description: "Tu compra se ha realizado con éxito 🎉",
                    type: "success",
                    duration: 3000,
                    floating: true,
                });
            }
        } catch (error) {
            console.error('Error en la compra:', error);
            showMessage({
                message: "Error",
                description: error instanceof Error ? error.message : "Error en la compra del carrito",
                type: "danger",
                duration: 3000,
                floating: true,
            });
            // No resetear el carrito en caso de error
        }
    };

    const renderItem = (item: Trago | Producto, tipo: 'trago' | 'producto') => {
        const searchTerm = tipo === 'trago'
            ? `${item.nombre} ${(item as Trago).tipo} `
            : `${item.nombre} ${(item as Producto).marca} bar`;

        return (
            <View key={`${tipo}-${item.id}`} style={styles.itemCard}>
                <View style={styles.imageContainer}>
                    <ImageWithSearch searchTerm={searchTerm} />
                    {item.stock <= 5 && (
                        <View style={styles.stockBadge}>
                            <Text style={styles.stockBadgeText}>
                                {item.stock === 0 ? 'Sin stock' : `¡Solo ${item.stock}!`}
                            </Text>
                        </View>
                    )}
                </View>
                <View style={styles.itemInfo}>
                    <Text style={styles.itemName}>
                        {item.nombre}{' '}
                        <Text style={styles.itemDetail}>
                            ({tipo === 'trago' ? (item as Trago).tipo : (item as Producto).marca}) ({item.volumen}ml)
                        </Text>
                    </Text>
                    <Text style={styles.itemPrice}>${item.precio_unitario}</Text>
                    <Text style={styles.stockText}>Disponible: {item.stock}</Text>
                    <View style={styles.addToCartContainer}>
                        <TextInput
                            style={[
                                styles.quantityInput,
                                errors[item.nombre] ? styles.quantityInputError : null
                            ]}
                            keyboardType="numeric"
                            value={quantities[item.nombre] || ''}
                            onChangeText={(text) => {
                                const cleanText = text.replace(/[^0-9]/g, '');
                                setQuantities({
                                    ...quantities,
                                    [item.nombre]: cleanText
                                });
                                setErrors({
                                    ...errors,
                                    [item.nombre]: ''
                                });
                            }}
                            placeholder="0"
                            placeholderTextColor="#666"
                        />
                        <TouchableOpacity
                            style={[
                                styles.addButton,
                                item.stock === 0 && styles.addButtonDisabled
                            ]}
                            onPress={() => handleAddToCart(item, tipo)}
                            disabled={item.stock === 0}
                        >
                            <Text style={styles.addButtonText}>
                                {item.stock === 0 ? 'Sin stock' : 'Añadir'}
                            </Text>
                        </TouchableOpacity>
                    </View>
                    {errors[item.nombre] ? (
                        <Text style={styles.errorText}>{errors[item.nombre]}</Text>
                    ) : null}
                </View>
            </View>
        );
    };

    const renderCartItem = (item: CartItem) => (
        <View key={`cart-${item.tipo}-${item.id}`} style={styles.cartItemCard}>
            <View style={styles.cartItemInfo}>
                <Text style={styles.cartItemName}>
                    {item.nombre} ({item.detalle}) ({item.volumen}ml)
                </Text>
                <Text style={styles.cartItemDetail}>
                    {item.cantidad} x ${item.precio_unitario} = ${item.cantidad * item.precio_unitario}
                </Text>
            </View>
            <TouchableOpacity
                style={styles.removeButton}
                onPress={() => handleRemoveFromCart(item.id, item.tipo)}
            >
                <Text style={styles.removeButtonText}>×</Text>
            </TouchableOpacity>
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Bar</Text>
            </View>

            <ScrollView contentContainerStyle={styles.scrollContent}>
                <Image
                    source={require('@/assets/images/bar.jpg')}
                    style={styles.bannerImage}
                    resizeMode="cover"
                />

                <View style={styles.content}>
                    <Text style={styles.sectionTitle}>Tragos</Text>
                    {tragos && tragos.map((trago) => renderItem(trago, 'trago'))}

                    <Text style={styles.sectionTitle}>Productos</Text>
                    {productos && productos.map((producto) => renderItem(producto, 'producto'))}

                    {cart.length > 0 && (
                        <>
                            <Text style={styles.sectionTitle}>Añadidos</Text>
                            <View style={styles.cartSection}>
                                {cart.map(renderCartItem)}
                                <View style={styles.totalContainer}>
                                    <Text style={styles.totalText}>Total: ${totalAmount}</Text>
                                </View>
                            </View>
                        </>
                    )}
                </View>

                {/* Espacio adicional al final para que el último elemento sea visible */}
                <View style={{ height: 100 }} />
            </ScrollView>

            {/* Botón de compra fijo en la parte inferior */}
            <View style={styles.purchaseContainer}>
                <TouchableOpacity
                    style={[styles.purchaseButton, cart.length === 0 && styles.purchaseButtonDisabled]}
                    onPress={handlePurchase}
                    disabled={cart.length === 0}
                >
                    <Text style={styles.purchaseButtonText}>
                        {cart.length > 0 ? 'Comprar 🛒' : 'Añade productos al 🛒'}
                    </Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'black',
    },
    scrollContent: {
        flexGrow: 1,
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
    bannerImage: {
        width: width,
        height: 200,
    },
    content: {
        padding: 20,
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginTop: 20,
        marginBottom: 16,
    },
    itemCard: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 16,
        marginBottom: 16,
        flexDirection: 'row',
    },
    //itemImage: {
    //    width: 80,
    //    height: 80,
    //    borderRadius: 8,
    //    marginRight: 16,
    //},
    itemInfo: {
        flex: 1,
    },
    itemName: {
        fontSize: 18,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 4,
    },
    itemDetail: {
        fontSize: 16,
        color: '#999',
        fontWeight: 'normal',
    },
    itemPrice: {
        fontSize: 16,
        color: '#B57EDC',
        marginBottom: 8,
    },
    addToCartContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    quantityInput: {
        backgroundColor: '#333',
        borderRadius: 8,
        padding: 8,
        width: 60,
        marginRight: 12,
        color: 'white',
        textAlign: 'center',
    },
    addButton: {
        backgroundColor: '#7C03D6',
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 8,
    },
    addButtonText: {
        color: 'white',
        fontSize: 14,
        fontWeight: 'bold',
    },
    cartSection: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 16,
        marginBottom: 16,
    },
    cartItemCard: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingVertical: 8,
        borderBottomWidth: 1,
        borderBottomColor: '#333',
    },
    cartItemInfo: {
        flex: 1,
    },
    cartItemName: {
        fontSize: 16,
        color: 'white',
        marginBottom: 4,
    },
    cartItemDetail: {
        fontSize: 14,
        color: '#B57EDC',
    },
    removeButton: {
        padding: 8,
    },
    removeButtonText: {
        color: '#FF4444',
        fontSize: 24,
        fontWeight: 'bold',
    },
    totalContainer: {
        marginTop: 16,
        paddingTop: 16,
        borderTopWidth: 1,
        borderTopColor: '#333',
    },
    totalText: {
        fontSize: 18,
        fontWeight: 'bold',
        color: 'white',
        textAlign: 'right',
    },
    purchaseContainer: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'black',
        paddingHorizontal: 20,
        paddingVertical: 10,
        borderTopWidth: 1,
        borderTopColor: '#333',
    },
    purchaseButton: {
        backgroundColor: '#7C03D6',
        padding: 16,
        borderRadius: 12,
        alignItems: 'center',
    },
    purchaseButtonDisabled: {
        backgroundColor: '#444',
    },
    purchaseButtonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
    stockText: {
        fontSize: 14,
        color: '#999',
        marginBottom: 8,
    },
    errorText: {
        color: '#FF4444',
        fontSize: 12,
        marginTop: 4,
    },
    quantityInputError: {
        borderWidth: 1,
        borderColor: '#FF4444',
    },
    imageContainer: {
        position: 'relative',
        marginRight: 16,
    },
    itemImage: {
        width: 80,
        height: 80,
        borderRadius: 8,
        backgroundColor: '#2A2A2A', // Color de fondo mientras carga
    },
    stockBadge: {
        position: 'absolute',
        top: 0,
        right: 0,
        backgroundColor: '#FF4444',
        paddingHorizontal: 6,
        paddingVertical: 2,
        borderRadius: 4,
    },
    stockBadgeText: {
        color: 'white',
        fontSize: 10,
        fontWeight: 'bold',
    },
    addButtonDisabled: {
        backgroundColor: '#444',
        opacity: 0.7,
    },
});

export default BarScreen;


/*

import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    ScrollView,
    Image,
    StyleSheet,
    Dimensions,
    TouchableOpacity,
    TextInput,
    StatusBar,
    SafeAreaView,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';

const { width, height } = Dimensions.get('window');

interface CartItem {
    id: string;
    nombre: string;
    cantidad: number;
    precio_unitario: number;
    tipo: 'trago' | 'producto';
}

const BarScreen = () => {
    const { tragos, productos } = useAuth();
    const [cart, setCart] = useState<CartItem[]>([]);
    const [quantities, setQuantities] = useState<{ [key: string]: string }>({});
    const [totalAmount, setTotalAmount] = useState(0);

    useEffect(() => {
        // Calcular el monto total cada vez que el carrito cambie
        const newTotal = cart.reduce((acc, item) => {
            return acc + (item.precio_unitario * item.cantidad);
        }, 0);
        setTotalAmount(newTotal);
    }, [cart]);

    const handleAddToCart = (item: Trago | Producto, tipo: 'trago' | 'producto') => {
        const quantity = parseInt(quantities[item.nombre] || '0');
        if (quantity <= 0) return;

        const existingItem = cart.find(cartItem => cartItem.nombre === item.nombre);
        if (existingItem) {
            setCart(cart.map(cartItem =>
                cartItem.nombre === item.nombre
                    ? { ...cartItem, cantidad: cartItem.cantidad + quantity }
                    : cartItem
            ));
        } else {
            setCart([...cart, {
                id: Math.random().toString(),
                nombre: item.nombre,
                cantidad: quantity,
                precio_unitario: item.precio_unitario,
                tipo
            }]);
        }
        setQuantities({ ...quantities, [item.nombre]: '' });
    };

    const handlePurchase = () => {
        // Aquí implementarías la lógica de compra
        console.log('Items en el carrito:', cart);
        console.log('Monto total:', totalAmount);
        // Reset cart after purchase
        setCart([]);
        setQuantities({});
    };

    const renderItem = (item: Trago | Producto, tipo: 'trago' | 'producto') => (
        <View key={item.nombre} style={styles.itemCard}>
            <Image
                source={tipo === 'trago'
                    ? require('@/assets/images/drink.jpg')
                    : require('@/assets/images/bebidas_1.jpg')
                }
                style={styles.itemImage}
            />
            <View style={styles.itemInfo}>
                <Text style={styles.itemName}>{item.nombre}{' '}
                    <Text style={styles.itemDetail}>
                        ({tipo === 'trago' ? (item as Trago).tipo : (item as Producto).marca})
                    </Text>
                </Text>
                <Text style={styles.itemPrice}>${item.precio_unitario}</Text>
                <View style={styles.addToCartContainer}>
                    <TextInput
                        style={styles.quantityInput}
                        keyboardType="numeric"
                        value={quantities[item.nombre] || ''}
                        onChangeText={(text) => setQuantities({
                            ...quantities,
                            [item.nombre]: text.replace(/[^0-9]/g, '')
                        })}
                        placeholder="0"
                        placeholderTextColor="#666"
                    />
                    <TouchableOpacity
                        style={styles.addButton}
                        onPress={() => handleAddToCart(item, tipo)}
                    >
                        <Text style={styles.addButtonText}>Añadir</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Bar</Text>
            </View>

            <ScrollView contentContainerStyle={styles.scrollContent}>
                <Image
                    source={require('@/assets/images/bar.jpg')}
                    style={styles.bannerImage}
                    resizeMode="cover"
                />

                <View style={styles.content}>
                    <Text style={styles.sectionTitle}>Tragos</Text>
                    {tragos && tragos.map((trago) => renderItem(trago, 'trago'))}

                    <Text style={styles.sectionTitle}>Productos</Text>
                    {productos && productos.map((producto) => renderItem(producto, 'producto'))}
                </View>

                {/* Espacio adicional al final para que el último elemento sea visible 
                <View style={{ height: 100 }} />
            </ScrollView>

            {/* Botón de compra fijo en la parte inferior 
            <View style={styles.purchaseContainer}>
                <TouchableOpacity
                    style={styles.purchaseButton}
                    onPress={handlePurchase}
                >
                    <Text style={styles.purchaseButtonText}>
                        Comprar {cart.length > 0 ? `(${cart.reduce((acc, item) => acc + item.cantidad, 0)} items - $${totalAmount})` : ''}
                    </Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'black',
    },
    scrollContent: {
        flexGrow: 1,
    },
    itemDetail: {
        fontSize: 16,
        color: '#999',
        fontWeight: 'normal',
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
    bannerImage: {
        width: width,
        height: 200,
    },
    content: {
        padding: 20,
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginTop: 20,
        marginBottom: 16,
    },
    itemCard: {
        backgroundColor: '#1A1A1A',
        borderRadius: 12,
        padding: 16,
        marginBottom: 16,
        flexDirection: 'row',
    },
    itemImage: {
        width: 80,
        height: 80,
        borderRadius: 8,
        marginRight: 16,
    },
    itemInfo: {
        flex: 1,
    },
    itemName: {
        fontSize: 18,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 4,
    },
    itemPrice: {
        fontSize: 16,
        color: '#B57EDC',
        marginBottom: 8,
    },
    addToCartContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    quantityInput: {
        backgroundColor: '#333',
        borderRadius: 8,
        padding: 8,
        width: 60,
        marginRight: 12,
        color: 'white',
        textAlign: 'center',
    },
    addButton: {
        backgroundColor: '#7C03D6',
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 8,
    },
    addButtonText: {
        color: 'white',
        fontSize: 14,
        fontWeight: 'bold',
    },
    purchaseContainer: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'black',
        paddingHorizontal: 20,
        paddingVertical: 10,
        borderTopWidth: 1,
        borderTopColor: '#333',
    },
    purchaseButton: {
        backgroundColor: '#7C03D6',
        padding: 16,
        borderRadius: 12,
        alignItems: 'center',
    },
    purchaseButtonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
});

export default BarScreen; */