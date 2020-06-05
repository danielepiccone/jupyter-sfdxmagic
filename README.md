# jupyter-sfdxmagic

## Description

This is a set of cell magics to run anonymous APEX code in notebooks and perform SOQL queries returning the records in a pandas DataFrame.

## Prerequisite

Authentication and connection to Salesforce are performed through sfdx, the magics assume sfdx is correctly installed and at least the default organization has been authorized.

## Usage

To load the extension:

```
%load_ext sfdxmagic
```

### `%%sfdx:apex`

Runs anonymous APEX:

```
%%sfdx:apex
System.debug('hello world!');
```

Append the name of a variable to return the log lines as a list

```
%%sfdx:apex logs
...
```

### `%%sfdx:query`

Perform a SOQL query:

```
%%sfdx:query
SELECT Id FROM Lead LIMIT 10
```

Append the name of a variable to return the records as a pandas DataFrame

```
%%sfdx:query df_records
...
```

### General invocation

All the parameters passed to the commands are forwarded to sfdx, this allows to combine results from multiple organizations for analysis.

```
%%sfdx:query df_records_org1 --targetusername org1
...
```

```
%%sfdx:query df_records_org2 --targetusername org2
...
```
