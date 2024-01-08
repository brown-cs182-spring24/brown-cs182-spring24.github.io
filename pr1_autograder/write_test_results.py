import sys
import json

if __name__ == '__main__':
    local_correct = 0
    seeding_correct = 0
    extension_correct = 0
    j = dict()
    j["score"] = 0
    j["visibility"] = "hidden"
    j["stdout_visibility"] = "hidden"
    j["tests"] = []
    for i in range(30):
        idx = 4 * i + 1
        passed = sys.argv[idx]
        input = sys.argv[idx+1]
        result = sys.argv[idx+2]
        expected = sys.argv[idx+3]
        output = passed
        test = dict()
        if passed == "Test case passed":
            local_correct += 1
            test["status"] = "passed"
        else:
            test["status"] = "failed"
        test["number"] = "1." + str(i+1)
        test["name"] = "Local Alignment Test " + str(i+1)
        test["output"] = output + \
            "\n\nInput: " + input + \
            "\n\nGot:\n" + result + \
            "\n\nExpected:\n" + expected
        if i == 0 or i == 1 or i == 3 or i == 5 or i == 20 or i == 21:
            test["visibility"] = "visible"
        j["tests"].append(test)
    for i in range(36):
        idx = 4 * i + 121
        passed = sys.argv[idx]
        input = sys.argv[idx+1]
        result = sys.argv[idx+2]
        expected = sys.argv[idx+3]
        output = passed
        test = dict()
        if passed == "Test case passed":
            seeding_correct += 1
            test["status"] = "passed"
        else:
            test["status"] = "failed"
        test["number"] = "2." + str(i+1)
        test["name"] = "Seeding Test " + str(i+1)
        test["output"] = output + \
            "\n\nInput: " + input + \
            "\n\nGot:\n" + result + \
            "\n\nExpected:\n" + expected
        if i == 0 or i == 12:
            test["visibility"] = "visible"
        j["tests"].append(test)
    for i in range(15):
        idx = 4 * i + 261
        passed = sys.argv[idx]
        input = sys.argv[idx+1]
        result = sys.argv[idx+2]
        expected = sys.argv[idx+3]
        output = passed
        test = dict()
        if passed == "Test case passed":
            extension_correct += 1
            test["status"] = "passed"
        else:
            test["status"] = "failed"
        test["number"] = "3." + str(i+1)
        test["name"] = "Extension Test " + str(i+1)
        test["output"] = output + \
            "\n\nInput: " + input + \
            "\n\nGot:\n" + result + \
            "\n\nExpected:\n" + expected
        if i == 0:
            test["visibility"] = "visible"
        j["tests"].append(test)
    j["score"] = 15 * (local_correct/30) + 35 * (seeding_correct/36) + 35 * (extension_correct/15)
    with open("results.json", "w") as f:
        json.dump(j, f)
    print("Local Alignment: " + str(local_correct) + "/30 test cases passed")
    print("Seeding: " + str(seeding_correct) + "/36 test cases passed")
    print("Extension: " + str(extension_correct) + "/15 test cases passed")
