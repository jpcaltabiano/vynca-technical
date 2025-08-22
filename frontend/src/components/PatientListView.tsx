import * as React from "react";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";
import { DataGrid, type GridColDef, type GridRowParams, type GridCellParams } from '@mui/x-data-grid';
import { Modal, Box, Typography, Button } from "@mui/material";

const PATIENTS_QUERY = gql`
    query {
        patients {
            id
            patientId
            firstName
            lastName
            dob
            email
            phone
            address
            isComplete
            appointmentCount
        }
    }
`;

type PatientGql = {
    id: string;
    patientId: string | null;
    firstName?: string | null;
    lastName?: string | null;
    dob?: string | null;
    email?: string | null;
    phone?: string | null;
    address?: string | null;
    isComplete: boolean;
    appointmentCount: number;
};

type PatientsQueryData = { patients: PatientGql[] };

type Props = {
    onSelect: (id: string) => void;
};

// future work - generate this from the data object directly instead of hardcoding
const patientColumns: GridColDef[] = [
    {
        field: "patientId",
        headerName: "Patient ID",
        width: 90,
        align: 'right',
        headerAlign: 'right',
        renderCell: (params) => (
            <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 6, width: '100%' }}>
                {params.row.isComplete ? null : <span title="Incomplete">⚠️</span>}
                <span>{params.value ?? ""}</span>
            </div>
        ),
    },
    { field: "firstName", headerName: "First Name", width: 110 },
    { field: "lastName", headerName: "Last Name", width: 140 },
    { field: "dob", headerName: "DOB", width: 130 },
    { field: "email", headerName: "Email", width: 220 },
    { field: "phone", headerName: "Phone", width: 150 },
    { field: "address", headerName: "Address", width: 140 },
    {
        field: "appointmentCount",
        headerName: "Appointments",
        width: 130,
        type: "number",
    },
];

function toPatientRows(patients: PatientGql[]) {
    return patients.map((p) => ({
        id: p.id,
        patientId: p.patientId ?? "",
        firstName: p.firstName ?? "",
        lastName: p.lastName ?? "",
        dob: p.dob ?? "",
        email: p.email ?? "",
        phone: p.phone ?? "",
        address: p.address ?? "",
        isComplete: Boolean(p.isComplete),
        appointmentCount: p.appointmentCount ?? 0,
    }));
}

export default function PatientListView({ onSelect }: Props) {
    const { data, loading, error } = useQuery<PatientsQueryData>(PATIENTS_QUERY);
    const [isWarningModalOpen, setIsWarningModalOpen] = React.useState(false);

    if (loading) return <div>Loading patients…</div>;
    if (error) return <div>Error loading patients</div>;

    const patients = data?.patients ?? [];
    const rows = toPatientRows(patients);

    const handleCellClick = (params: GridCellParams, event: React.MouseEvent) => {
        // open modal when clicking id cell on an incomplete patient row
        if (params.field === 'patientId' && (params.row as any)?.isComplete === false) {
            event.stopPropagation();
            setIsWarningModalOpen(true);
        }
    };

    const modalStyle = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
        borderRadius: 8,
    };

    return (
        <div style={{ width: "100%" }}>
            <DataGrid
                rows={rows}
                columns={patientColumns}
                onRowClick={(params) => onSelect(String(params.id))}
                onCellClick={handleCellClick}
                getRowId={(row) => row.id}
                getRowClassName={(params) => (params.row.isComplete ? "" : "row-incomplete")}
                sx={{
                    '& .row-incomplete': {
                        backgroundColor: 'rgba(180, 31, 2, 0.3)'
                    }
                }}
                initialState={{
                    pagination: { paginationModel: { pageSize: 10 } },
                }}
                pageSizeOptions={[5, 10, 25]}
                disableRowSelectionOnClick
            />

            {isWarningModalOpen && (
                <div>
                    <Modal open={isWarningModalOpen} onClose={() => setIsWarningModalOpen(false)}>
                        <Box sx={modalStyle}>
                            <Typography id="modal-title" variant="h6" component="h2">
                                Patient record warning
                            </Typography>
                            <Typography id="modal-description" sx={{ mt: 2 }}>
                                This patient's record is incomplete. Please review the patient's information and update the missing fields.

                                Patient must have, at minimum, a last name, DOB, and either an email or phone number.
                            </Typography>
                            <Box sx={{ mt: 3, textAlign: 'right' }}>
                                <Button
                                    variant="contained"
                                    color="primary"
                                    onClick={() => setIsWarningModalOpen(false)}
                                >
                                    Close
                                </Button>
                            </Box>
                        </Box>
                    </Modal>
                </div>
            )}
        </div>
    );
}


