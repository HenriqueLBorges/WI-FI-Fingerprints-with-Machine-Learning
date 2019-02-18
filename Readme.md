# USO-DE-TECNOLOGIA-ASSISTIVA-PARA-GUIAR-ALUNOS-COM-DEFICIENCIA-VISUAL-NO-CAMPUS-SENAC-SANTO-AMARO

This project implements indoor navigation using Wi-Fi Fingerprints collected and Machine Learning models to recognize current user position and guide it to your destination. In order to achieve the objective a series of steps are needed.

1. Collect Wi-Fi Fingerprints to a specific interest point (site-survey).
2. Save the collected Wi-Fi Fingerprints using a noSQL MongoDB.
3. Join all MongoDB into a big JSON Array.
4. Convert the JSON Array indo a CSV dataset.
5. Train machine learning models using the CSV dataset.
6. Expose the machine learning models through an REST API.
7. Collect new Wi-Fi Fingerprints using a rapsberry pi and submit them to the REST API in order to indentify the current position.

All Wi-Fi Fingerprints collected are distribuited according their interest points. Those interest points corresponds to the building rooms entrance. All JSON documents collected on the site-survey can be found [here](https://tcc-dataset-wifi-fingerprints.s3.amazonaws.com).

This project is part of my undergraduate thesis. All it's code is structured in four different folders.

* Machine Learning - Responsible for all data transformation and model training.

* Site-survey CLI - The tool used in the processo of building site-survey.

* REST API - Used to execute the machine learning model exposing it using endpoints.

* Raspberry PI - The python program responsible to collect Wi-Fi Fingerprints and submit them to the API in order to guide the user through the building.