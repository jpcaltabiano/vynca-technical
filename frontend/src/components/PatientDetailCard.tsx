import * as React from "react";
import { Card, CardContent, Typography, Box, Chip, Stack } from "@mui/material";
import EmailIcon from "@mui/icons-material/Email";
import PhoneIcon from "@mui/icons-material/Phone";
import LocationOnIcon from "@mui/icons-material/LocationOn";

type Props = {
    firstName?: string | null;
    lastName?: string | null;
    dob?: string | null;
    email?: string | null;
    phone?: string | null;
    address?: string | null;
    appointmentCount?: number;
};

// future work would show empty fields if email/phone/address are null
export default function PatientDetailCard({ firstName, lastName, dob, email, phone, address, appointmentCount }: Props) {
    const fullName = `${firstName ?? ""} ${lastName ?? ""}`.trim() || "Unknown";
    const apptLabel = `${appointmentCount ?? 0} appointment${(appointmentCount ?? 0) === 1 ? "" : "s"}`;

    return (
        <Card sx={{ maxWidth: 480, borderRadius: 3, boxShadow: 3, p: 2, mb: 2 }}>
            <CardContent>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <Box>
                        <Typography variant="h6" fontWeight="bold">{fullName}</Typography>
                        {dob && (
                            <Typography variant="body2" color="text.secondary">DOB {dob}</Typography>
                        )}
                    </Box>
                    <Chip label={apptLabel} color="primary" size="small" sx={{ fontWeight: "bold" }} />
                </Box>

                <Stack spacing={1.5} mt={2}>
                    {email && (
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                            <EmailIcon fontSize="small" color="action" />
                            <Typography variant="body2">{email}</Typography>
                        </Box>
                    )}

                    {phone && (
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                            <PhoneIcon fontSize="small" color="action" />
                            <Typography variant="body2">{phone}</Typography>
                        </Box>
                    )}

                    {address && (
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                            <LocationOnIcon fontSize="small" color="action" />
                            <Typography variant="body2">{address}</Typography>
                        </Box>
                    )}
                </Stack>
            </CardContent>
        </Card>
    );
}
