import React, { useEffect, useState } from "react";
import {axiosPublic} from "./AppRouter.tsx";
import {
    Container,
    TextField,
    Button,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress, CssBaseline, Box, ButtonGroup, Select, MenuItem,
} from "@mui/material";
import { Link } from "react-router-dom";
import Moment from 'moment';


interface DashboardPageProps {
    logout: () => void;
}

const DashboardPage: React.FC<DashboardPageProps> = ({ logout }) => {
    Moment.locale('en');

    const [searchTerm, setSearchTerm] = useState<string>("");
    const [results, setResults] = useState<[]>([]);
    const [language, setLanguage] = useState<string>("EN-US");
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const changeLanguage = (lng) => {
        setLanguage(lng);  // Change language in i18next
    };

    const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null); // Reset error message on new search

        try {
            const response = await axiosPublic.get(`/api/search/`, {
                params: {
                    language,
                    query: searchTerm
                },
                headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
            });
            setResults(response.data); // Adjust based on your API response structure
        } catch (err) {
            setError("Error fetching search results.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container>
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    height: "100vh", // Full height
                    width: "100vw",
                    padding: 2,
                }}
            >
                <CssBaseline/>
                <Typography variant="h4" gutterBottom sx={{textAlign: "left"}}>
                    Dashboard
                </Typography>
                <form onSubmit={handleSearch} style={{width: "100%"}}>
                    <Box
                        sx={{
                            display: "flex",
                            flexDirection: "row",
                            justifyContent: "flex-start",
                            width: "100%",
                            alignItems: "center"
                        }}
                    >
                        <TextField
                            variant="outlined"
                            label="Search"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            margin="normal"
                            sx={{
                                width: "70%",
                                margin: "0",
                                height: "56px", // Adjust height as needed
                                "& .MuiInputBase-root": {height: "56px"}, // Ensure input field has the same height
                            }}
                        />
                        <Select
                            labelId="language-select-label"
                            variant="outlined"
                            id="language-select"
                            value={language}
                            onChange={(event) => changeLanguage(event.target.value)}
                            label="Language"
                            sx={{
                                ml: 1
                            }}
                        >
                            <MenuItem value="EN-US">English</MenuItem>
                            <MenuItem value="RU">Русский</MenuItem>
                            <MenuItem value="RO">Română</MenuItem>
                        </Select>
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            sx={{height: "56px", ml: 1}} // Button occupies full width
                        >
                            Search
                        </Button>
                    </Box>
                </form>

                {loading && <CircularProgress style={{marginTop: '20px'}}/>}
                {error && (
                    <Typography color="error" style={{marginTop: '20px'}}>
                        {error}
                    </Typography>
                )}
                {!loading && results.length > 0 && (
                    <>
                        {results.map((item) => (
                            <Box
                                sx={{
                                    display: "flex",
                                    flexDirection: "row",
                                    justifyContent: "flex-center",
                                    width: "80%",
                                    height: "100px",
                                    alignItems: "center"
                                }}
                            >
                                <Box
                                    sx={{
                                        display: "flex",
                                        flexDirection: "row",
                                        justifyContent: "flex-start",
                                        width: "50%",
                                        alignItems: "end"
                                    }}
                                >
                                    <Box>
                                        <Typography sx={{ fontSize: "20px", fontWeight: "600"}}>{item[0].metadata.name}</Typography>
                                        <Typography>{item[0].metadata.job_position}</Typography>
                                    </Box>
                                    <Box sx={{ ml: 5}}>
                                        <Typography color="secondary">Accuracy: {Math.round(item[1] * 100)}%</Typography>
                                    </Box>
                                </Box>
                                <Box
                                    sx={{
                                        display: "flex",
                                        flexDirection: "row",
                                        justifyContent: "flex-end",
                                        width: "50%",
                                        alignItems: "center"
                                    }}
                                >
                                    <Box>
                                        <Typography>sent</Typography>
                                        <Typography>{Moment(item[0].metadata.created_at).format('YYYY/DD/MM HH:mm')}</Typography>
                                    </Box>
                                    <Box
                                        sx={{
                                            marginLeft: "20px"
                                        }}
                                    >
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            component={Link}
                                            to={`/view/${item[0].metadata.id}`} // Replace with your actual route
                                        >
                                            view
                                        </Button>
                                    </Box>
                                </Box>
                            </Box>
                        ))}
                    </>
                )}
                {!loading && results.length === 0 && (
                    <Typography style={{marginTop: '20px'}}>
                        No results found.
                    </Typography>
                )}
            </Box>
        </Container>
    );
};


export default DashboardPage;
