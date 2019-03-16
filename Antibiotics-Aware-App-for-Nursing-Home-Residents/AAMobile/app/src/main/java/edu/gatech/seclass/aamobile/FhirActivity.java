package edu.gatech.seclass.aamobile;

import java.util.List;
import java.util.HashSet;
import java.util.ArrayList;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.model.dstu2.resource.Bundle;
import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.model.primitive.IdDt;
import ca.uhn.fhir.model.dstu2.resource.Observation;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import ca.uhn.fhir.util.BundleUtil;

public class FhirActivity {

    private IGenericClient client;
    private FhirContext ctx;
    List<IdDt> IDs = new ArrayList<>();
    List<String> uniqueIDs = new ArrayList<>();
    HashSet uniqueIDset = new HashSet();
    HashSet patientNameset = new HashSet();
    List<String> uniqueIDarray = new ArrayList<>();
    List<String> patientNamearray = new ArrayList<>();
    List<String> patientName = new ArrayList<>();


    public FhirActivity() {
        ctx = FhirContext.forDstu2();
        client = ctx.newRestfulGenericClient("http://fhirtest.uhn.ca/baseDstu2");
    }

    public List<String> getPatients() {
        String loincIdUrl = "http://fhirtest.uhn.ca/baseDstu2/Observation?code=38483-4";

        Bundle bundle = client.search()
                .byUrl(loincIdUrl)
                .returnBundle(Bundle.class)
                .execute();
        if (bundle.getLink(Bundle.LINK_NEXT) != null) {
            Bundle nextPage = client.loadPage().next(bundle).execute();
        }
        System.out.println("Found " + bundle.getEntry().size() + " patients named 'duck'");

        int bundleSize = bundle.getEntry().size();

        for (int n = 0; n <= bundleSize - 1; n++) {
            Observation observation = (Observation) bundle
                    .getEntry()
                    .get(n)
                    .getResource();
            IDs.add(observation.getSubject().getReference());
            //measurement.add(observation.getValue());
        }

        while (bundle.getLink(Bundle.LINK_NEXT) != null) {
            bundle = client.loadPage().next(bundle).execute();
            bundleSize = bundle.getEntry().size();
            for (int n = 0; n <= bundleSize - 1; n++) {
                Observation observation = (Observation) bundle
                        .getEntry()
                        .get(n)
                        .getResource();
                IDs.add(observation.getSubject().getReference());
                //measurement.add(observation.);
            }
        }
        HashSet hashSet = new HashSet(IDs);
        System.out.println("IDs" + hashSet);

        for (int i = 0; i < IDs.size(); i++){
            String patientID = IDs.get(i).toString();
            patientID = patientID.replaceAll("[^0-9]", "");
            uniqueIDs.add(patientID);
        }
        uniqueIDset = new HashSet(uniqueIDs);
        uniqueIDarray = new ArrayList<>(uniqueIDset);

        for (int i = 0; i < uniqueIDarray.size(); i++) {
            String patName = getNameByPatientID(uniqueIDarray.get(i));
            patientName.add(patName);
        }
        patientNameset = new HashSet(patientName);
        patientNamearray = new ArrayList<>(patientNameset);
        System.out.println("Name: " + patientNamearray);

        return uniqueIDarray;
    }


    public String getNameByPatientID(String id) {
        String name = null;
        Patient patient = client.read().resource(Patient.class).withId(id)
                .execute();

        name = patient.getNameFirstRep().getNameAsSingleString();
        return name;
    }

    public IGenericClient getClient() {
        return client;
    }
}
