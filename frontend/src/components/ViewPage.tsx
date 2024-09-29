import React, {useEffect, useState} from "react";
import {
    Avatar,
    Box,
    Chip,
    Container,
    Divider,
    Grid,
    Typography,
    Paper,
    Stack, CircularProgress
} from '@mui/material';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

import { useParams } from "react-router-dom";
import {axiosPublic} from "./AppRouter.tsx";

interface CV {
    [prop: string]: any;
}

const ViewPage: React.FC = () => {
    // Get the 'id' parameter from the URL
    const { id } = useParams<{ id: string }>();

    const [cv, setCV] = useState<CV | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchCV = async () => {
            try {
                const response = await axiosPublic.get(`/api/cvs/${id}`, {
                    headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
                }); // Replace with your actual API URL
                console.log(response.data)
                setCV(response.data); // Set the fetched data to state
            } catch (error) {
                setError('Failed to fetch profile data.');
            } finally {
                setLoading(false); // Stop loading after fetching data or if there's an error
            }
        };

        if (!cv) {
            setLoading(true);
            fetchCV();
            setLoading(false);
        }
    })

    return (
        <Container sx={{ mt: 4, width: "100%" }}>
            {loading && <CircularProgress style={{marginTop: '20px'}}/>}
            {error && (
                <Typography color="error" style={{marginTop: '20px'}}>
                    {error}
                </Typography>
            )}

            {!loading && cv && (
                <Paper elevation={3} sx={{ p: 4 }}>
                    {/* Header */}
                    <Grid container alignItems="center" justifyContent="space-between" mb={2}>
                        <Typography variant="h5">{cv.job_position}</Typography>
                        <Typography variant="body2">-</Typography>
                    </Grid>

                    <Grid container spacing={2} alignItems="center">
                        <Grid item>
                            <Avatar
                                alt={cv.name}
                                src="/path/to/avatar.jpg" // You can add the avatar image path here
                                sx={{ width: 80, height: 80 }}
                            />
                        </Grid>
                        <Box
                            sx={{
                                ml: 2,
                                display: "flex",
                                flexDirection: "column",
                                alignItems: "right",
                                justifyContent: "flex-start"
                            }}
                        >
                            <Grid item>
                                <Typography variant="h6">{cv.name}</Typography>
                                <Typography variant="body2">-</Typography>
                                <Typography variant="body2">{cv.email}</Typography>
                                <Typography variant="body2">{cv.phone_number}</Typography>
                            </Grid>
                        </Box>
                    </Grid>

                    <Divider sx={{ my: 2 }} />

                    {/* Education */}
                    <Box mb={2}>
                        <Typography variant="h6">Education</Typography>
                        {cv.education.map((education) => (
                            <Typography variant="body2">
                                {education.institution}, {education.education}
                            </Typography>
                        ))}
                    </Box>

                    {/* Experience */}
                    <Box mb={2}>
                        <Typography variant="h6" sx={{ mb: 2 }}>Experience</Typography>
                        <Grid container spacing={1}>
                            {cv.work_experience.map((experience, index) => (
                                <Grid item key={index}>
                                    <Box
                                        sx={{
                                            display: "flex",
                                            flexDirection: "column",
                                            justifyContent: "space-between",
                                            alignItems: "center"
                                        }}
                                    >
                                        <Chip label={experience.company} color="primary" />
                                        <Chip label={experience.title} variant="outlined" sx={{ ml: 1, mt: "10px" }} />
                                        <Typography variant="body2">{experience.start_date ?? ''} - {experience.end_date ?? ''}</Typography>
                                    </Box>
                                </Grid>
                            ))}
                        </Grid>
                    </Box>

                    {/* Roles and Responsibilities */}
                    <Box mb={2}>
                        <Typography variant="h6">Summary</Typography>
                        <p>{cv.summary}</p>
                    </Box>

                    {/* Soft Skills */}
                    <Box mb={2}>
                        <Typography variant="h6">Skills</Typography>
                        <Stack direction="row" spacing={1} flexWrap="wrap">
                            {cv.skills.map((skill, index) => (
                                <Chip key={index} label={skill} color="info" />
                            ))}
                        </Stack>
                    </Box>

                    {/* Languages */}
                    <Box mb={2}>
                        <Typography variant="h6">Languages</Typography>
                        {cv.languages && cv.languages.map((language) => (
                            <Typography variant="body2">language</Typography>
                        ))}
                        {!cv.languages && (
                            <Typography variant="body2">None</Typography>
                        )}
                    </Box>
                </Paper>
            )}
        </Container>
    );
};

export default ViewPage;
