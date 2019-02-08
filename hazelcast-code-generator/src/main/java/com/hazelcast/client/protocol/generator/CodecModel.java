/*
 * Copyright (c) 2008-2019, Hazelcast, Inc. All Rights Reserved.
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

import com.hazelcast.annotation.ContainsNullable;
import com.hazelcast.annotation.EventResponse;
import com.hazelcast.annotation.GenerateCodec;
import com.hazelcast.annotation.Nullable;
import com.hazelcast.annotation.Request;
import com.hazelcast.annotation.Since;

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

public class CodecModel
        implements Model {
    static final Map<String, TypeElement> CUSTOM_CODEC_MAP = new HashMap<String, TypeElement>();

    private static final String DEFAULT_PACKAGE_NAME = "com.hazelcast.client.impl.protocol.codec";
    private static final String DEFAULT_SINCE_VERSION = "1.0";
    private static final int EVENT_MODEL_TYPE = 104;

    private final List<ParameterModel> requestParams = new LinkedList<ParameterModel>();
    private final Map<String, List<ParameterModel>> versionedRequestParams = new HashMap<String, List<ParameterModel>>();
    private final List<ParameterModel> responseParams = new LinkedList<ParameterModel>();
    private final Map<String, List<ParameterModel>> versionedResponseParams = new HashMap<String, List<ParameterModel>>();
    private final List<EventModel> events = new LinkedList<EventModel>();

    private final Lang lang;
    private final String name;
    private final String parentName;
    private final String className;
    private final String packageName;

    private final int retryable;
    private final int acquiresResource;
    private final int response;

    private String messageSince = DEFAULT_SINCE_VERSION;
    private int messageSinceInt;
    private int highestParameterVersion = -1;

    private short requestId;
    private String id;
    private String partitionIdentifier;
    private String comment = "";

    private Elements elementUtil;

    CodecModel(TypeElement parent, ExecutableElement methodElement, ExecutableElement responseElement,
               List<ExecutableElement> eventElementList, boolean retryable, boolean acquiresResourse,
               Lang lang, Elements docCommentUtil) {
        GenerateCodec generateCodecAnnotation = parent.getAnnotation(GenerateCodec.class);
        Since codecSinceVersion = parent.getAnnotation(Since.class);
        Since methodSince = methodElement.getAnnotation(Since.class);
        messageSince = null != codecSinceVersion ? codecSinceVersion.value() : messageSince;
        messageSince = null != methodSince ? methodSince.value() : messageSince;
        Request requestAnnotation = methodElement.getAnnotation(Request.class);

        this.lang = lang;
        this.name = methodElement.getSimpleName().toString();
        this.parentName = generateCodecAnnotation.name();
        this.className = capitalizeFirstLetter(parentName) + capitalizeFirstLetter(name) + "Codec";
        this.packageName = (lang != Lang.JAVA) ? generateCodecAnnotation.ns() : DEFAULT_PACKAGE_NAME;

        this.retryable = retryable ? 1 : 0;
        this.acquiresResource = acquiresResourse ? 1 : 0;
        this.response = requestAnnotation.response();
        this.requestId = requestAnnotation.id();
        this.id = addHexPrefix(CodeGenerationUtils.mergeIds(generateCodecAnnotation.id(), requestId));
        this.partitionIdentifier = requestAnnotation.partitionIdentifier();

        this.elementUtil = docCommentUtil;

        this.messageSinceInt = CodeGenerationUtils.versionAsInt(messageSince);

        this.highestParameterVersion = messageSinceInt;

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
        this.acquiresResource = 0;
        this.response = EVENT_MODEL_TYPE;

        initRequestParameters();
        initResponseParameters();
        initEventModel();
    }

    private void initParameters(ExecutableElement methodElement, ExecutableElement responseElement,
                                List<ExecutableElement> eventElementList, Lang lang) {
        // request parameters
        initRequestParameters(methodElement, lang);

        // response parameters
        initResponseParameters(responseElement, lang);

        // event parameters
        initEventParameters(eventElementList, lang);
    }

    private void initEventParameters(List<ExecutableElement> eventElementList, Lang lang) {
        for (ExecutableElement element : eventElementList) {
            EventModel eventModel = new EventModel();
            eventModel.comment = elementUtil.getDocComment(element);
            Since eventSinceVersion = element.getAnnotation(Since.class);
            eventModel.sinceVersion = eventSinceVersion != null ? eventSinceVersion.value() : DEFAULT_SINCE_VERSION;
            eventModel.sinceVersionInt = CodeGenerationUtils.versionAsInt(eventModel.sinceVersion);
            eventModel.type = element.getAnnotation(EventResponse.class).value();
            eventModel.name = element.getSimpleName().toString();

            List<ParameterModel> eventParam = new ArrayList<ParameterModel>();
            int previousParamVersionInt = eventModel.sinceVersionInt;
            String previousParamVersion = eventModel.sinceVersion;

            for (VariableElement param : element.getParameters()) {
                Nullable nullable = param.getAnnotation(Nullable.class);
                Since sinceVersion = param.getAnnotation(Since.class);
                ContainsNullable containsNullable = param.getAnnotation(ContainsNullable.class);
                String paramVersion = eventModel.sinceVersion;
                if (null != sinceVersion) {
                    paramVersion = sinceVersion.value();
                }

                String parameterName = param.getSimpleName().toString();
                ParameterModel pm = createParameterModel(parameterName, param.asType().toString(), nullable != null,
                        containsNullable != null, paramVersion, lang);

                int paramVersionInt = pm.sinceVersionInt;
                if (paramVersionInt > highestParameterVersion) {
                    highestParameterVersion = paramVersionInt;
                }
                if (paramVersionInt != previousParamVersionInt) {
                    pm.versionChanged = true;
                    eventModel.versionedEventParams.put(previousParamVersion, new LinkedList<ParameterModel>(eventParam));
                }
                previousParamVersionInt = paramVersionInt;
                previousParamVersion = paramVersion;
                eventParam.add(pm);
            }
            eventModel.versionedEventParams.put(previousParamVersion, new LinkedList<ParameterModel>(eventParam));
            eventModel.eventParams = eventParam;
            events.add(eventModel);
        }
    }

    private void initResponseParameters(ExecutableElement responseElement, Lang lang) {
        Since responseSinceAnnotation = responseElement.getAnnotation(Since.class);
        String previousParamVersion = responseSinceAnnotation != null ? responseSinceAnnotation.value() : messageSince;
        int previousParamVersionInt = CodeGenerationUtils.versionAsInt(previousParamVersion);
        for (VariableElement param : responseElement.getParameters()) {
            Nullable nullable = param.getAnnotation(Nullable.class);
            Since sinceVersion = param.getAnnotation(Since.class);
            ContainsNullable containsNullable = param.getAnnotation(ContainsNullable.class);
            String paramVersion = previousParamVersion;
            if (null != sinceVersion) {
                paramVersion = sinceVersion.value();
            }
            String parameterName = param.getSimpleName().toString();
            ParameterModel pm = createParameterModel(parameterName, param.asType().toString(), nullable != null,
                    containsNullable != null, paramVersion, lang);
            int paramVersionInt = pm.sinceVersionInt;
            if (paramVersionInt > highestParameterVersion) {
                highestParameterVersion = paramVersionInt;
            }
            if (paramVersionInt != previousParamVersionInt) {
                pm.versionChanged = true;
                versionedResponseParams.put(previousParamVersion, new LinkedList<ParameterModel>(responseParams));
            }
            previousParamVersionInt = paramVersionInt;
            previousParamVersion = paramVersion;
            responseParams.add(pm);
        }
        versionedResponseParams.put(previousParamVersion, new LinkedList<ParameterModel>(responseParams));
    }

    private void initRequestParameters(ExecutableElement methodElement, Lang lang) {
        int previousParamVersionInt = 1 * CodeGenerationUtils.MAJOR_VERSION_MULTIPLIER;
        String previousParamVersion = messageSince;
        for (VariableElement param : methodElement.getParameters()) {
            Nullable nullable = param.getAnnotation(Nullable.class);
            Since sinceVersion = param.getAnnotation(Since.class);
            ContainsNullable containsNullable = param.getAnnotation(ContainsNullable.class);
            String paramVersion = messageSince;
            if (null != sinceVersion) {
                paramVersion = sinceVersion.value();
            }
            String parameterName = escape(param.getSimpleName().toString(), lang);
            ParameterModel pm = createParameterModel(parameterName, param.asType().toString(), nullable != null,
                    containsNullable != null, paramVersion, lang);
            int paramVersionInt = pm.sinceVersionInt;
            if (paramVersionInt > highestParameterVersion) {
                highestParameterVersion = paramVersionInt;
            }
            if (paramVersionInt != previousParamVersionInt) {
                pm.versionChanged = true;
                versionedRequestParams.put(previousParamVersion, new LinkedList<ParameterModel>(requestParams));
            }
            previousParamVersionInt = paramVersionInt;
            previousParamVersion = paramVersion;
            requestParams.add(pm);
        }
        versionedRequestParams.put(previousParamVersion, new LinkedList<ParameterModel>(requestParams));
    }

    private void initRequestParameters() {
        requestParams.add(createParameterModel("name", "java.lang.String", true, DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("val", "int", false, DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("address", "com.hazelcast.nio.Address", false, DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("arr", "int[]", false, DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("setD", "java.util.Set<" + DATA_FULL_NAME + ">", false, DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("mapIS", "java.util.Map<java.lang.Integer, java.lang.String>", false,
                DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("mapDD", "java.util.Map<" + DATA_FULL_NAME + ", " + DATA_FULL_NAME + ">", false,
                DEFAULT_SINCE_VERSION));
        requestParams.add(createParameterModel("entryView",
                "com.hazelcast.map.impl.SimpleEntryView<" + DATA_FULL_NAME + ", " + DATA_FULL_NAME + ">", true,
                DEFAULT_SINCE_VERSION));
    }

    private void initResponseParameters() {
        responseParams.add(createParameterModel("name", "long", false, DEFAULT_SINCE_VERSION));
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

    public Map<String, List<ParameterModel>> getVersionedRequestParams() {
        return versionedRequestParams;
    }

    public List<ParameterModel> getResponseParams() {
        return responseParams;
    }

    public Map<String, List<ParameterModel>> getVersionedResponseParams() {
        return versionedResponseParams;
    }

    public List<EventModel> getEvents() {
        return events;
    }

    public int getRetryable() {
        return retryable;
    }

    public int getAcquiresResource() {
        return acquiresResource;
    }

    public String getMessageSince() {
        return messageSince;
    }

    public int getMessageSinceInt() {
        return messageSinceInt;
    }

    public int getHighestParameterVersion() {
        return highestParameterVersion;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    private static ParameterModel createParameterModel(String name, String type, boolean nullAble,
                                                       String since) {
        return createParameterModel(name, type, nullAble, false, since, Lang.JAVA);
    }

    private static ParameterModel createParameterModel(String name, String type,
                                                       boolean nullAble, boolean containsNullable, String since, Lang lang) {
        ParameterModel pm = new ParameterModel();
        pm.name = name;
        pm.type = type;
        pm.lang = lang;
        pm.nullable = nullAble;
        pm.containsNullable = containsNullable;
        pm.sinceVersion = since;
        pm.sinceVersionInt = CodeGenerationUtils.versionAsInt(pm.sinceVersion);
        return pm;
    }

    public static class EventModel {

        private String name;
        private List<ParameterModel> eventParams;
        private final Map<String, List<ParameterModel>> versionedEventParams = new HashMap<String, List<ParameterModel>>();
        private int type;
        private String comment = "";
        private String sinceVersion = DEFAULT_SINCE_VERSION;
        private int sinceVersionInt;

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

        public Map<String, List<ParameterModel>> getVersionedEventParams() {
            return versionedEventParams;
        }

        public String getComment() {
            return comment;
        }

        public String getSinceVersion() {
            return sinceVersion;
        }

        public int getSinceVersionInt() {
            return sinceVersionInt;
        }

    }

    public static class ParameterModel {

        private String name;
        private String type;
        private Lang lang;
        private boolean nullable;
        private String description = "";
        private String sinceVersion = DEFAULT_SINCE_VERSION;
        private int sinceVersionInt;
        // By default versionChanged is false
        private boolean versionChanged;
        private boolean containsNullable;

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

        public String getSinceVersion() {
            return sinceVersion;
        }

        public int getSinceVersionInt() {
            return sinceVersionInt;
        }

        public boolean isVersionChanged() {
            return versionChanged;
        }

        public boolean getContainsNullable() {
            return containsNullable;
        }

    }
}
