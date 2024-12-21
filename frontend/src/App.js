import React, { useState } from "react";
import config from "./config";
import axios from "axios";
import {
    Container,
    TextField,
    Button,
    Grid,
    Card,
    CardContent,
    CardMedia,
    Typography,
    CircularProgress,
    Box,
} from "@mui/material";

function App() {
    const [listings, setListings] = useState([]);
    const [filters, setFilters] = useState({
        city: "lahore",
        minPrice: 0,
        maxPrice: 100000000,
    });
    const [loading, setLoading] = useState(false); // Track loading state

    const fetchListings = async () => {
        setLoading(true); // Show loader when search is initiated
        try {
            const response = await axios.get(
				`${config.API_BASE_URL}/api/listings?city=${filters.city}&min_price=${filters.minPrice}&max_price=${filters.maxPrice}`
			);
            setListings(response.data.listings);
        } catch (error) {
            console.error("Error fetching listings:", error);
        } finally {
            setLoading(false); // Hide loader after fetching is done
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFilters((prev) => ({ ...prev, [name]: value }));
    };

    const handleSearch = () => {
        fetchListings(); // Trigger the fetch when Search is clicked
    };

    return (
        <Container maxWidth="lg">
            <Typography variant="h4" gutterBottom align="center" style={{ marginTop: "20px" }}>
                Real Estate Listing Analyzer
            </Typography>
            <Grid container spacing={2} style={{ marginBottom: "20px" }}>
                <Grid item xs={12} sm={4}>
                    <TextField
                        fullWidth
                        label="City"
                        name="city"
                        value={filters.city}
                        onChange={handleInputChange}
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <TextField
                        fullWidth
                        type="number"
                        label="Min Price"
                        name="minPrice"
                        value={filters.minPrice}
                        onChange={handleInputChange}
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <TextField
                        fullWidth
                        type="number"
                        label="Max Price"
                        name="maxPrice"
                        value={filters.maxPrice}
                        onChange={handleInputChange}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Button
                        fullWidth
                        variant="contained"
                        color="primary"
                        onClick={handleSearch}
                        style={{ height: "50px" }}
                    >
                        Search
                    </Button>
                </Grid>
            </Grid>
            {loading ? (
                // Show loader when loading after clicking search
                <Box display="flex" justifyContent="center" alignItems="center" style={{ marginTop: "50px" }}>
                    <CircularProgress />
                </Box>
            ) : (
                <Grid container spacing={3}>
                    {listings.length > 0 ? (
                        listings.map((listing, index) => (
                            <Grid item xs={12} sm={6} md={4} key={index}>
                                <Card>
                                    <CardMedia
                                        component="img"
                                        height="140"
                                        image={listing.img_url || "https://via.placeholder.com/150"}
                                        alt={listing.title}
                                    />
                                    <CardContent>
                                        <Typography gutterBottom variant="h6">
                                            {listing.title}
                                        </Typography>
                                        <Button
                                            variant="contained"
                                            color="secondary"
                                            href={listing.link}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            View Details
                                        </Button>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))
                    ) : (
                        <Typography variant="body1" align="center" style={{ width: "100%" }}>
                            No listings found.
                        </Typography>
                    )}
                </Grid>
            )}
        </Container>
    );
}

export default App;
