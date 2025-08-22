import * as React from "react";
import {ApolloClient, InMemoryCache, HttpLink} from "@apollo/client";
import {ApolloProvider} from "@apollo/client/react";
import { createTheme, ThemeProvider, CssBaseline } from "@mui/material";
import PatientListView from "./components/PatientListView";
import PatientDetailView from "./components/PatientDetailView";


const client = new ApolloClient({
    link: new HttpLink({ uri: "/graphql" }),
    cache: new InMemoryCache()
});

export default function App() {
    const [selectedPatientId, setSelectedPatientId] = React.useState<string | null>(null);
    const theme = React.useMemo(() => createTheme({
        palette: {
            mode: 'dark',
            background: {
                default: '#2a2438',
                paper: '#332d41'
            },
            text: {
                primary: '#e6e1e8'
            }
        },
        typography: {
            fontFamily: 'Roboto'
        }
    }), []);
    return (
        <ApolloProvider client={client}>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, height: '100vh', padding: 16, boxSizing: 'border-box' }}>
                    <div style={{ overflow: 'auto' }}>
                        <h2>Patients</h2>
                        <PatientListView onSelect={(id) => setSelectedPatientId(id)} />
                    </div>
                    <div style={{ borderLeft: '1px solid #49454f', paddingLeft: 16, overflow: 'auto' }}>
                        <h2>Patient Details</h2>
                        <PatientDetailView patientId={selectedPatientId} />
                    </div>
                </div>
            </ThemeProvider>
        </ApolloProvider>
    );
}
