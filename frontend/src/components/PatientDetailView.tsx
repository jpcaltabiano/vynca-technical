import * as React from "react";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const PATIENT_QUERY = gql`
    query GetPatient($id: UUID!) {
        patient(id: $id) {
            patientId
            firstName
            lastName
            isComplete
            appointments { appointmentId appointmentDate appointmentType }
        }
    }
`;

type Appointment = {
    id: string;
    appointmentId: string;
    appointmentDate?: string | null;
    appointmentType?: string | null;
};

type Patient = {
    id: string;
    patientId?: string | null;
    firstName?: string | null;
    lastName?: string | null;
    isComplete: boolean;
    appointments: Appointment[];
};

type PatientQueryData = { patient: Patient | null };
type PatientQueryVars = { id: string };

type Props = {
    patientId: string | null;
};

export default function PatientDetailView({ patientId }: Props) {
    // runs the gql query using apollo client
    // passes patient UUID as string, and skips if falsy
    const { data, loading, error } = useQuery<PatientQueryData, PatientQueryVars>(PATIENT_QUERY, {
        variables: { id: patientId as string },
        skip: !patientId
    });

    // fallbacks
    if (!patientId) return <div>Select a patient to view details.</div>;
    if (loading) return <div>Loading details…</div>;
    if (error) return <div>Error loading details</div>;

    const p = data?.patient;
    if (!p) return <div>No patient found.</div>;

    return (
        <div>
            <div style={{ marginBottom: 12, fontWeight: 600 }}>{p.firstName ?? ''} {p.lastName ?? ''}</div>
            <div style={{ marginBottom: 8 }}>Appointments</div>
            <TableContainer component={Paper}>
                <Table size="small" aria-label="appointments table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Appointment ID</TableCell>
                            <TableCell>Appointment Date</TableCell>
                            <TableCell>Appointment Type</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {(p.appointments ?? []).map((a) => (
                            <TableRow key={a.appointmentId}>
                                <TableCell>{a.appointmentId}</TableCell>
                                <TableCell>{a.appointmentDate ?? ''}</TableCell>
                                <TableCell>{a.appointmentType ?? ''}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
}

