import json
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify

app = Flask(__name__)
print("ggchgdf")
# generate schema
@app.route('/generate_schema', methods=['POST'])
def generate_schema():
    print ("reaching")
    # parse XML input from user
    xml_input = request.get_data()
    root = ET.fromstring(xml_input)
    print(root)
    # convert XML schema to JSON schema
    schema = {}
    for child in root:
        situation = child.attrib['name']
        schema[situation] = {}
        for element in child:
            schema[situation][element.tag] = {
                "data_type": element.attrib.get('type', 'string'),
                "operator": element.attrib.get('operator', '')
            }

    with open('schema-updated.json', 'w') as f:
        json.dump(schema, f, indent=4)

    return jsonify(schema)

# generate queries based on JSON schema
@app.route('/generate_queries', methods=['POST'])
def generate_queries():
    with open('schema-updated.json', 'r') as f:
        schema = json.load(f)

    num_of_queries = request.args.get('num_of_queries', default=3, type=int)

    queries = []
    for situation in schema:
        for i in range(num_of_queries):
            query = {"situation": situation, "timestamp": "", "query": {}}
            for attributes in schema[situation]:
                data_type = schema[situation][attributes]["data_type"]
                if data_type == "string":
                    query["query"][attributes] = ""
                elif data_type == "datetime":
                    query["query"][attributes] = {"operator": schema[situation][attributes]["operator"], "value": ""}
                elif data_type == "geo-coordinate":
                    query["query"]["latitude"] = {"operator": schema[situation]["latitude"]["operator"], "value": ""}
                    query["query"]["longitude"] = {"operator": schema[situation]["longitude"]["operator"], "value": ""}
            queries.append(query)

    with open('queries-updated.csv', 'w') as f:
        f.write("situation,timestamp,query\n")
        for query in queries:
            f.write("{},{},{}\n".format(query["situation"], query["timestamp"], json.dumps(query["query"])))

    return jsonify({'queries-updated': queries})


if __name__ == '__main__':
    app.run()








