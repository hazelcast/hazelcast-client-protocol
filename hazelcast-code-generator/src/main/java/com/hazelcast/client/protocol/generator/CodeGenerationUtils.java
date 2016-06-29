/*
 * Copyright (c) 2008-2015, Hazelcast, Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.hazelcast.client.protocol.generator;

import javax.lang.model.element.TypeElement;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

@SuppressWarnings("checkstyle:methodcount")
public final class CodeGenerationUtils {

    /**
     * Package prefix for the codec module.
     */
    public static final String CODEC_PACKAGE = "com.hazelcast.client.impl.protocol.codec.";

    /**
     * Fully qualified classname for Hazelcast Data class.
     */
    public static final String DATA_FULL_NAME = "com.hazelcast.nio.serialization.Data";

    /**
     * The multiplier is used to convert a version string to a comparable integer number
     */
    public static final int MAJOR_VERSION_MULTIPLIER = 1000;

    private static final int BYTE_BIT_COUNT = 8;

    @SuppressWarnings("checkstyle:whitespacearound")
    private static final Map<String, String> JAVA_TO_PYTHON_TYPES = new HashMap<String, String>() { {
        put(DATA_FULL_NAME, "Data");
        put("java.lang.String", "str");
        put("java.lang.Integer", "int");
        put("boolean", "bool");
        put("java.util.List", "list");
        put("java.util.Set", "set");
        put("java.util.Collection", "collection");
        put("java.util.Map", "dictionary");
        put("java.util.Map.Entry", "tuple");
        put("com.hazelcast.nio.Address", "Address");
        put("com.hazelcast.client.impl.client.DistributedObjectInfo", "DistributedObjectInfo");
        put("com.hazelcast.core.Member", "Member");
        put("com.hazelcast.cluster.client.MemberAttributeChange", "MemberAttributeChange");
        put("com.hazelcast.map.impl.SimpleEntryView", "SimpleEntryView");
    } };

    private static final Map<String, String> JAVA_TO_NODE_TYPES = new HashMap<String, String>() { {
        put(DATA_FULL_NAME, "data");
        put("java.lang.String", "string");
        put("java.lang.Integer", "int32");
        put("boolean", "boolean");
        put("int", "int32");
        put("com.hazelcast.nio.Address", "Address");
        put("java.util.List", "list");
        put("java.util.Set", "set");
    } };

    private static final Map<String, String> JAVA_TO_TS_TYPES = new HashMap<String, String>() { {
        put(DATA_FULL_NAME, "Data");
        put("java.lang.String", "string");
        put("java.lang.Integer", "number");
        put("boolean", "boolean");
        put("int", "number");
        put("com.hazelcast.nio.Address", "Address");
        put("java.util.List", "any");
        put("java.util.Collection", "any[]");
        put("java.util.Set", "any");
        put("long", "any");
    } };

    @SuppressWarnings("checkstyle:whitespacearound")
    private static final Map<String, String> JAVA_TO_CSHARP_TYPES = new HashMap<String, String>() { {
        put(DATA_FULL_NAME, "IData");
        put("java.lang.String", "string");
        put("java.lang.Integer", "int");
        put("boolean", "bool");
        put("java.util.List", "IList");
        put("java.util.Set", "ISet");
        put("java.util.Collection", "ICollection");
        put("java.util.Map", "IDictionary");
        put("java.util.Map.Entry", "KeyValuePair");
        put("com.hazelcast.nio.Address", "Address");
        put("com.hazelcast.client.impl.client.DistributedObjectInfo", "DistributedObjectInfo");
        put("com.hazelcast.core.Member", "Core.IMember");
        put("com.hazelcast.cluster.client.MemberAttributeChange", "Hazelcast.Client.Request.Cluster.MemberAttributeChange");
        put("com.hazelcast.map.impl.SimpleEntryView", "Hazelcast.Map.SimpleEntryView");
    } };

    @SuppressWarnings({"checkstyle:whitespacearound", "checkstyle:executablestatementcount"})
    private static final Map<String, String> JAVA_TO_CPP_TYPES = new HashMap<String, String>() { {
        put("java.lang.Integer", "int32_t");
        put("int", "int32_t");
        put("boolean", "bool");
        put("java.lang.Boolean", "bool");
        put("short", "int16_t");
        put("char", "int8_t");
        put("byte", "uint8_t");
        put("long", "int64_t");
        put(DATA_FULL_NAME, "serialization::pimpl::Data");
        put("java.lang.String", "std::string");
        put("byte[]", "std::vector<byte>");
        put("java.util.List", "std::vector");
        put("java.util.Set", "std::vector");
        put("java.util.Collection", "std::vector");
        put("java.util.Map", "std::vector<std::pair");
        put("java.util.Map.Entry", "std::pair");
        put("com.hazelcast.nio.Address", "Address");
        put("com.hazelcast.client.impl.client.DistributedObjectInfo", "impl::DistributedObjectInfo");
        put("com.hazelcast.core.Member", "Member");
        put("com.hazelcast.cluster.client.MemberAttributeChange", "MemberAttributeChange");
        put("com.hazelcast.map.impl.SimpleEntryView", "EntryView");
    } };

    private static final List<String> PYTHON_RESERVED_WORDS = Arrays
            .asList("and", "del", "from", "not", "while", "as", "elif", "global", "or", "with", "assert", "else", "if", "pass",
                    "yield", "break", "except", "import", "print", "class", "exec", "in", "raise", "continue", "finally", "is",
                    "return", "def", "for", "lambda", "try");

    private CodeGenerationUtils() {
    }

    public static String capitalizeFirstLetter(String input) {
        return input.substring(0, 1).toUpperCase() + input.substring(1);
    }

    public static String getPackageNameFromQualifiedName(String qualifiedClassName) {
        return qualifiedClassName.substring(0, qualifiedClassName.lastIndexOf("."));
    }

    public static String mergeIds(short classId, short methodId) {
        return Integer.toHexString((classId << BYTE_BIT_COUNT) + methodId);
    }

    public static String addHexPrefix(String s) {
        switch (s.length()) {
            case 3:
                return "0x0" + s;
            case 2:
                return "0x00" + s;
            case 1:
                return "0x000" + s;
            default:
                return "0x" + s;
        }
    }

    public static String getArrayType(String type) {
        int end = type.indexOf("[]");
        return type.substring(0, end).trim();
    }

    public static String getGenericType(String type) {
        int beg = type.indexOf("<");
        int end = type.lastIndexOf(">");
        return type.substring(beg + 1, end).trim();
    }

    public static String getSimpleType(String type) {
        int beg = type.indexOf("<");
        return type.substring(0, beg);
    }

    public static String getFirstGenericParameterType(String type) {
        int beg = type.indexOf("<");
        int end = type.lastIndexOf(",");
        return type.substring(beg + 1, end).trim();
    }

    public static String getSecondGenericParameterType(String type) {
        int beg = type.indexOf(",");
        int end = type.lastIndexOf(">");
        return type.substring(beg + 1, end).trim();
    }

    public static boolean isPrimitive(String type) {
        return type.equals("int") || type.equals("long") || type.equals("short") || type.equals("byte") || type.equals("boolean");
    }

    public static boolean isGeneric(String type) {
        return type.contains("<");
    }

    public static String getTypeCategory(String type) {
        int endIndex = type.indexOf('<');
        String t = endIndex > 0 ? type.substring(0, endIndex) : type;
        if (CodecModel.CUSTOM_CODEC_MAP.containsKey(t)) {
            return "CUSTOM";
        } else if (t.equals("java.util.Map.Entry")) {
            return "MAPENTRY";
        } else if (t.equals("java.util.List") || t.equals("java.util.Set") || t.equals("java.util.Collection")) {
            return "COLLECTION";
        } else if (type.endsWith("[]")) {
            return "ARRAY";
        }
        return "OTHER";
    }

    public static String getTypeCodec(String type) {
        int endIndex = type.indexOf('<');
        String t = endIndex > 0 ? type.substring(0, endIndex) : type;
        TypeElement typeElement = CodecModel.CUSTOM_CODEC_MAP.get(t);
        return typeElement != null ? typeElement.toString() : "";
    }

    public static String getConvertedType(String type) {
        if (type.startsWith("java.util.List<") || type.startsWith("java.util.Set<") || type.startsWith("java.util.Collection<")) {
            return type.replaceAll("java.util.*<(.*)>", "java.util.Collection<$1>");
        }
        return type;
    }

    public static String getDescription(String parameterName, String commentString) {
        String result = "";
        if (parameterName == null || commentString == null) {
            return result;
        }
        int start = commentString.indexOf("@param");
        if (start == -1) {
            return result;
        }
        String paramString = commentString.substring(start);
        String[] paramStrings = paramString.split("@param");
        for (String parameterString : paramStrings) {
            /**
             * Example such string is
             * key      key of the entry
             */

            String trimmedParameterString = parameterString.trim();
            if (trimmedParameterString.length() > parameterName.length() && trimmedParameterString.startsWith(parameterName)) {
                result = trimmedParameterString.substring(parameterName.length());
                int endIndex = result.indexOf('@');
                if (endIndex >= 0) {
                    result = result.substring(0, endIndex);
                }

                // replace any new line with <br>
                result = result.replace("\n", "<br>");
                result = result.trim();

                // found the parameter, hence stop here
                break;
            }
        }
        return result;
    }

    public static String getReturnDescription(String commentString) {
        String result = "";
        String returnTag = "@return";
        int returnTagStartIndex = commentString.indexOf(returnTag);
        if (returnTagStartIndex >= 0) {
            int descriptionStartIndex = returnTagStartIndex + returnTag.length();
            int nextTagIndex = commentString.indexOf("@", descriptionStartIndex);
            if (nextTagIndex >= 0) {
                result = commentString.substring(descriptionStartIndex, nextTagIndex);
            } else {
                result = commentString.substring(descriptionStartIndex);
            }
            result = result.trim();

            // replace any new line with <br>
            result = result.replace("\n", "<br>");
        }
        return result;
    }

    public static String getOperationDescription(String commentString) {
        String result = "";
        int nextTagIndex = commentString.indexOf("@");
        if (nextTagIndex >= 0) {
            result = commentString.substring(0, nextTagIndex);

            result = result.trim();
        }

        result = result.replace("\n", "<br>");

        return result;
    }

    public static String getDistributedObjectName(String templateClassName) {
        String result = templateClassName;
        if (templateClassName.equals("com.hazelcast.client.impl.protocol.template.ClientMessageTemplate")) {
            return "Generic";
        }
        int startIndex = templateClassName.lastIndexOf('.');
        if (startIndex >= 0) {
            int endIndex = templateClassName.indexOf("CodecTemplate", startIndex);
            if (endIndex > startIndex) {
                result = templateClassName.substring(startIndex + 1, endIndex);
            }
        }

        return result;
    }

    // parse generic type parameters, making sure nested generics are taken into account
    private static List<String> getGenericTypeParameters(String parameters) {
        List<String> paramList = new ArrayList<String>();
        int balanced = 0;
        StringBuilder current = new StringBuilder();
        for (int i = 0; i < parameters.length(); i++) {
            char c = parameters.charAt(i);
            if (balanced == 0 && c == ',') {
                paramList.add(current.toString().trim());
                current = new StringBuilder();
                continue;
            } else if (c == '<') {
                balanced++;
            } else if (c == '>') {
                balanced--;
            }
            current.append(c);
        }
        paramList.add(current.toString());
        return paramList;
    }

    public static String getPythonType(String type) {
        return getLanguageType(Lang.PY, type, JAVA_TO_PYTHON_TYPES);
    }

    public static String getCSharpType(String type) {
        return getLanguageType(Lang.CS, type, JAVA_TO_CSHARP_TYPES);
    }

    public static String getCppType(String type) {
        return getLanguageType(Lang.CPP, type, JAVA_TO_CPP_TYPES);
    }

    public static String getNodeType(String type) {
        return getLanguageType(Lang.NODE, type, JAVA_TO_NODE_TYPES);
    }

    public static String getNodeTsType(String type) {
        return JAVA_TO_TS_TYPES.get(type) != null ? JAVA_TO_TS_TYPES.get(type) : "any";
    }

    public static String getLanguageType(Lang language, String type, Map<String, String> languageMapping) {
        type = type.trim();
        if (isGeneric(type)) {
            String simpleType = getLanguageType(language, getSimpleType(type), languageMapping);
            String genericParameters = getGenericType(type);

            List<String> typeParameters = getGenericTypeParameters(genericParameters);
            StringBuilder builder = new StringBuilder();

            builder.append(simpleType).append('<');

            Iterator<String> iterator = typeParameters.iterator();
            while (iterator.hasNext()) {
                builder.append(getLanguageType(language, iterator.next(), languageMapping));
                if (iterator.hasNext()) {
                    builder.append(", ");
                }
            }

            if (language == Lang.CPP && type.startsWith("java.util.Map<")) {
                builder.append(" > >");
            } else {
                builder.append(" >");
            }

            String result = builder.toString();
            if (result.equals("EntryView<serialization::pimpl::Data, serialization::pimpl::Data >")) {
                result = "map::DataEntryView";
            }

            return result;
        }

        String convertedType = languageMapping.get(type);

        return convertedType == null ? type : convertedType;
    }

    public static boolean shouldGenerateForCpp(String codecName) {
        return !(codecName.equals("MapReduce") || codecName.equals("Cache") || codecName.equals("Ringbuffer") || codecName
                .equals("EnterpriseMap") || codecName.equals("XATransaction"));
    }

    public static String convertToSnakeCase(String camelCase) {
        return camelCase.replaceAll("(.)(\\p{Upper})", "$1_$2").toLowerCase();
    }

    public static String convertToNodeType(String name) {
        //        name = convertToSnakeCase(name);
        if (name.equals("function")) {
            return "arr";
        }
        if (name.equals("arguments")) {
            return "args";
        }
        return name;
    }

    public static String escape(String str, Lang lang) {
        switch (lang) {
            case PY:
                return PYTHON_RESERVED_WORDS.contains(str) ? str + "_" : str;
            default:
                //TODO add other lang reserved words
                return str;
        }
    }

    /**
     *
     * @param messageSince The version of the message. E.g. 1.2
     * @return Int representation of the version. Calculated as: minor + (major * 1000).
     * E.g. 1002 for "1.2"
     */
    public static int versionAsInt(String messageSince) {
        String[] versions = messageSince.split("\\.");
        return Integer.parseInt(versions[1]) + Integer.parseInt(versions[0]) * MAJOR_VERSION_MULTIPLIER;
    }

    /**
     *
     * @param version protocol version as int. E.g. 1002
     * @return The protocol version as string, 1.2 for 1002
     */
    public static String versionAsString(int version) {
        return String.format("%d.%d", version / MAJOR_VERSION_MULTIPLIER, version % MAJOR_VERSION_MULTIPLIER);
    }

    /**
     *
     * @param version protocol version as int. E.g. 1002
     * @return The protocol version as string, 1_2 for 1002
     */
    public static String versionAsClassName(int version) {
        return String.format("%d_%d", version / MAJOR_VERSION_MULTIPLIER, version % MAJOR_VERSION_MULTIPLIER);
    }
}
