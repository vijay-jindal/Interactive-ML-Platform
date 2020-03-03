import CSVFileValidator from 'csv-file-validator'
CSVFileValidator(file,config)
	.then(csvdata => {
		csvdata.data
		csvdata.inValidMessages
	})
	.catch(err => {})
