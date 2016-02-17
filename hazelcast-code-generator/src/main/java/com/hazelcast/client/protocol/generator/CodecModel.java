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

import com.hazelcast.annotation.EventResponse;
import com.hazelcast.annotation.GenerateCodec;
import com.hazelcast.annotation.Nullable;
import com.hazelcast.annotation.Request;

import javax.lang.model.element.ExecutableElement;
import javax.lang.model.element.TypeElement;
import javax.lang.model.element.VariableElement;
import javax.lang.model.util.Elements;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import static com.hazelcast.client.protocol.generator.CodeGenerationUtils.DATA_FULL_NAME;
import static com.hazelcast.client.protocol.generator.CodeGenerationUtils.addHexPrefix;
import static com.hazelcast.client.protocol.generator.CodeGenerationUtils.capitalizeFirstLetter;
import static com.hazelcast.client.protocol.generator.CodeGenerationUtils.escape;

public class CodecModel implements Model {

    static final Map<String, TypeElement> CUSTOM_CODEC_MAP = new HashMap<String, TypeElement>();

    private static final String DEFAULT_PACKAGE_NAME = "com.hazelcast.client.impl.protocol.codec";
    private static final int EVENT_MODEL_TYPE = 104;

    private final List<ParameterModel> requestParams = new LinkedList<ParameterModel>();
    private final List<ParameterModel> responseParams = new LinkedList<ParameterModel>();
    private final List<EventModel> events = new LinkedList<EventModel>();

    private final Lang lang;
    private final String name;
    private final String parentName;
    private final String className;
    private final String packageName;

    private final int retryable;
    private final int response;

    private short requestId;
    private String id;
    private String partitionIdentifier;
    private String comment = "";

    private Elements elementUtil;

    CodecModel(TypeElement parent, ExecutableElement methodElement, ExecutableElement responseElement,
               List<ExecutableElement> eventElementList, boolean retryable, Lang lang, Elements docCommentUtil) {
        GenerateCodec generateCodecAnnotation = parent.getAnnotation(GenerateCodec.class);
        Request requestAnnotation = methodElement.getAnnotation(Request.class);

        this.lang = lang;
        this.name = methodElement.getSimpleName().toString();
        this.parentName = generateCodecAnnotation.name();
        this.className = capitalizeFirstLetter(parentName) + capitalizeFirstLetter(name) + "Codec";
        this.packageName = (lang != Lang.JAVA) ? generateCodecAnnotation.ns() : DEFAULT_PACKAGE_NAME;

        this.retryable = retryable ? 1 : 0;
        this.response = requestAnnotation.response();

        this.requestId = requestAnnotation.id();
        this.id = addHexPrefix(CodeGenerationUtils.mergeIds(generateCodecAnnotation.id(), requestId));
        this.partitionIdentifier = requestAnnotation.partitionIdentifier();

        this.elementUtil = docCommentUtil;

        initParameters(methodElement, responseElement, eventElementList, lang);
    }

    // TEST ONLY MOCKUP CONSTRUCTOR
    public CodecModel(boolean mockup) {
        this.lang = Lang.JAVA;
        this.name = "put";
        this.parentName = "Map";
        this.className = capitalizeFirstLetter(parentName) + capitalizeFirstLetter(name) + "Codec";
        this.packageName = DEFAULT_PACKAGE_NAME;

        this.retryable = 1;
        this.response = EVENT_MODEL_TYPE;

        initRequestParameters();
        initResponseParameters();
        initEventModel();
    }

    private void initParameters(ExecutableElement methodElement, ExecutableElement responseElement,
                                List<ExecutableElement> eventElementList, Lang lang) {
        // request parameters
        for (VariableElement param : methodElement.getParameters()) {
            Nullable nullable = param.getAnnotation(Nullable.class);
            String parameterName = escape(param.getSimpleName().toString(), lang);
            addParameterModel(requestParams, parameterName, param.asType().toString(), nullable != null, lang);
        }

        // response parameters
        for (VariableElement param : responseElement.getParameters()) {
            Nullable nullable = param.getAnnotation(Nullable.class);
            String parameterName = param.getSimpleName().toString();
            addParameterModel(responseParams, parameterName, param.asType().toString(), nullable != null, lang);
        }

        // event parameters
        for (ExecutableElement element : eventElementList) {
            EventModel eventModel = new EventModel();
            eventModel.comment = elementUtil.getDocComment(element);

            List<ParameterModel> eventParam = new ArrayList<ParameterModel>();
            for (VariableElement param : element.getParameters()) {
                Nullable nullable = param.getAnnotation(Nullable.class);
                ParameterModel pm = new ParameterModel();
                pm.name = param.getSimpleName().toString();
                pm.type = param.asType().toString();
                pm.lang = lang;
                pm.nullable = nullable != null;
                pm.description = CodeGenerationUtils.getDescription(pm.name, eventModel.comment);
                eventParam.add(pm);
            }

            eventModel.type = element.getAnnotation(EventResponse.class).value();
            eventModel.name = element.getSimpleName().toString();
            eventModel.eventParams = eventParam;

            events.add(eventModel);
        }
    }

    private void initRequestParameters() {
        addParameterModel(requestParams, "name", "java.lang.String", true);
        addParameterModel(requestParams, "val", "int", false);
        addParameterModel(requestParams, "address", "com.hazelcast.nio.Address", false);
        addParameterModel(requestParams, "arr", "int[]", false);
        addParameterModel(requestParams, "setD", "java.util.Set<" + DATA_FULL_NAME + ">", false);
        addParameterModel(requestParams, "mapIS", "java.util.Map<java.lang.Integer, java.lang.String>", false);
        addParameterModel(requestParams, "mapDD", "java.util.Map<" + DATA_FULL_NAME + ", " + DATA_FULL_NAME + ">", false);
        addParameterModel(requestParams, "entryView", "com.hazelcast.map.impl.SimpleEntryView<" + DATA_FULL_NAME + ", "
                + DATA_FULL_NAME + ">", true);
    }

    private void initResponseParameters() {
        addParameterModel(responseParams, "name", "long", false);
    }

    private void initEventModel() {
        ParameterModel pm = new ParameterModel();
        pm.name = "name";
        pm.type = "java.lang.String";
        pm.lang = Lang.JAVA;
        pm.nullable = true;

        List<ParameterModel> eventParam = new ArrayList<ParameterModel>();
        eventParam.add(pm);

        EventModel eventModel = new EventModel();
        eventModel.type = EVENT_MODEL_TYPE;
        eventModel.name = "";
        eventModel.eventParams = eventParam;
        events.add(eventModel);
    }

    public String getName() {
        return name;
    }

    public Lang getLang() {
        return lang;
    }

    public short getRequestId() {
        return requestId;
    }

    public String getId() {
        return id;
    }

    public String getPartitionIdentifier() {
        return partitionIdentifier;
    }

    public String getComment() {
        return comment;
    }

    public String getClassName() {
        return className;
    }

    public String getParentName() {
        return parentName;
    }

    public String getPackageName() {
        return packageName;
    }

    @Override
    public boolean isEmpty() {
        return requestParams.isEmpty();
    }

    public int getResponse() {
        return response;
    }

    public String getHexadecimalResponseId() {
        return addHexPrefix(Integer.toHexString(response));
    }

    public List<ParameterModel> getRequestParams() {
        return requestParams;
    }

    public List<ParameterModel> getResponseParams() {
        return responseParams;
    }

    public List<EventModel> getEvents() {
        return events;
    }

    public int getRetryable() {
        return retryable;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    private static void addParameterModel(List<ParameterModel> parameterModelList, String name, String type, boolean nullAble) {
        addParameterModel(parameterModelList, name, type, nullAble, Lang.JAVA);
    }

    private static void addParameterModel(List<ParameterModel> parameterModelList, String name, String type, boolean nullAble,
                                          Lang lang) {
        ParameterModel pm = new ParameterModel();
        pm.name = name;
        pm.type = type;
        pm.lang = lang;
        pm.nullable = nullAble;
        parameterModelList.add(pm);
    }

    public static class EventModel {

        private String name;
        private List<ParameterModel> eventParams;
        private int type;
        private String comment = "";

        public int getType() {
            return type;
        }

        public String getHexadecimalTypeId() {
            return addHexPrefix(Integer.toHexString(type));
        }

        public String getName() {
            return name;
        }

        public List<ParameterModel> getEventParams() {
            return eventParams;
        }

        public String getComment() {
            return comment;
        }
    }

    public static class ParameterModel {

        private String name;
        private String type;
        private Lang lang;
        private boolean nullable;
        private String description = "";

        public String getName() {
            return name;
        }

        public boolean isNullable() {
            return nullable;
        }

        public String getType() {
            return type;
        }

        public Lang getLang() {
            return lang;
        }

        public String getDescription() {
            return description;
        }
    }
}
