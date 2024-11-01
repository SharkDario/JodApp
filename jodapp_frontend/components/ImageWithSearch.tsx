import React, { useState, useEffect } from 'react';
import { View, Image, ActivityIndicator, StyleSheet } from 'react-native';

const ImageWithSearch: React.FC<{ searchTerm: string }> = ({ searchTerm }) => {
    const [imageUrl, setImageUrl] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(false);

    const PIXABAY_API_KEY = '46816235-e307b65c96a667d63db5c4b60'; // Tu API key

    useEffect(() => {
        const fetchImage = async () => {
            try {
                const encodedSearch = encodeURIComponent(searchTerm);
                // Modificada la URL para usar los parámetros correctos
                const apiUrl = `https://pixabay.com/api/?key=${PIXABAY_API_KEY}&q=${encodedSearch}&image_type=photo&safesearch=true`;

                console.log('Searching for:', searchTerm);
                console.log('API URL:', apiUrl);

                const response = await fetch(apiUrl);

                if (!response.ok) {
                    console.error('API Response not OK:', response.status);
                    const text = await response.text();
                    console.error('Response text:', text);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                if (data.hits && data.hits.length > 0) {
                    const url = data.hits[0].webformatURL;
                    setImageUrl(url);
                    setError(false);
                } else {
                    console.log('No images found for:', searchTerm);
                    setError(true);
                }
            } catch (err) {
                console.error('Error fetching image:', err);
                setError(true);
            } finally {
                setIsLoading(false);
            }
        };

        if (searchTerm) {
            fetchImage();
        }
    }, [searchTerm]);

    if (isLoading) {
        return (
            <View style={[styles.itemImage, { justifyContent: 'center', alignItems: 'center' }]}>
                <ActivityIndicator size="large" color="#0000ff" />
            </View>
        );
    }

    if (error || !imageUrl) {
        return (
            <Image
                source={require('@/assets/images/placeholder.jpg')}
                style={styles.itemImage}
            />
        );
    }

    return (
        <Image
            source={{
                uri: imageUrl,
                cache: 'force-cache'
            }}
            style={styles.itemImage}
            defaultSource={require('@/assets/images/placeholder.jpg')}
            onError={() => setError(true)}
        />
    );
};

const styles = StyleSheet.create({
    itemImage: {
        width: 150,
        height: 150,
        resizeMode: 'cover',
    }
});

export default ImageWithSearch;