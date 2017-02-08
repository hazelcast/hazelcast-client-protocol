/*
 * Copyright (c) 2008-2017, Hazelcast, Inc. All Rights Reserved.
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

import com.hazelcast.annotation.Codec;
import com.hazelcast.annotation.EventResponse;
import com.hazelcast.annotation.GenerateCodec;
import com.hazelcast.annotation.Request;
import com.hazelcast.annotation.Response;
import freemarker.cache.ClassTemplateLoader;
import freemarker.ext.beans.BeansWrapper;
import freemarker.log.Logger;
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateHashModel;
import freemarker.template.TemplateModelException;

import javax.annotation.processing.AbstractProcessor;
import javax.annotation.processing.Filer;
import javax.annotation.processing.Messager;
import javax.annotation.processing.ProcessingEnvironment;
import javax.annotation.processing.RoundEnvironment;
import javax.annotation.processing.SupportedAnnotationTypes;
import javax.annotation.processing.SupportedSourceVersion;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.ElementKind;
import javax.lang.model.element.ExecutableElement;
import javax.lang.model.element.TypeElement;
import javax.lang.model.type.MirroredTypeException;
import javax.lang.model.type.TypeMirror;
import javax.lang.model.util.Elements;
import javax.tools.Diagnostic;
import javax.tools.JavaFileManager;
import javax.tools.JavaFileObject;
import javax.tools.StandardLocation;
import java.io.IOException;
import java.io.Serializable;
import java.io.StringWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

import static com.hazelcast.client.protocol.generator.Lang.JAVA;

@SupportedAnnotationTypes("com.hazelcast.annotation.GenerateCodec")
@SupportedSourceVersion(SourceVersion.RELEASE_6)
public class CodecCodeGenerator extends AbstractProcessor {

    private static final int HEX_RADIX = 16;
    private static final String COMPATIBILITY_TEST_PACKAGE = "com.hazelcast.client.protocol.compatibility";
    private static final String GENERATE_COMPATIBILITY_TESTS = "protocol.compatibility.generate.tests";

    private boolean generateTests;
    private final Map<Lang, Template> codecTemplateMap = new HashMap<Lang, Template>();
    private final Map<Lang, Template> messageTypeTemplateMap = new HashMap<Lang, Template>();
    private class CompatibilityTestInfo {
        private final String fileName;
        private final boolean versioned;
        private Template template;

        public CompatibilityTestInfo(String fileName, boolean versioned) {
            this.fileName = fileName;
            this.versioned = versioned;
        }

        public String getFileName() {
            return fileName;
        }

        public boolean isVersioned() {
            return versioned;
        }

        public void setTemplate(Template template) {
            this.template = template;
        }

        public Template getTemplate() {
            return template;
        }
    }

    private final int[] protocolVersions = {
            CodeGenerationUtils.versionAsInt("1.0"), CodeGenerationUtils.versionAsInt("1.1"),
            CodeGenerationUtils.versionAsInt("1.2"), CodeGenerationUtils.versionAsInt("1.3"),
            CodeGenerationUtils.versionAsInt("1.4"),
    };

    private final CompatibilityTestInfo[] compatibilityTestInfos = {
                                         new CompatibilityTestInfo("ClientCompatibilityTest", true),
                                         new CompatibilityTestInfo("ClientCompatibilityNullTest", true),
                                         new CompatibilityTestInfo("EncodeDecodeCompatibilityTest", false),
                                         new CompatibilityTestInfo("EncodeDecodeCompatibilityNullTest", false),
                                         new CompatibilityTestInfo("BinaryCompatibilityFileGenerator", false),
                                         new CompatibilityTestInfo("BinaryCompatibilityNullFileGenerator", false),
                                         new CompatibilityTestInfo("ServerCompatibilityTest", true),
                                         new CompatibilityTestInfo("ServerCompatibilityNullTest", true),
                                         };

    private final Map<TypeElement, Map<Integer, ExecutableElement>> requestMap
            = new HashMap<TypeElement, Map<Integer, ExecutableElement>>();
    private final Map<Integer, ExecutableElement> responseMap = new HashMap<Integer, ExecutableElement>();
    private final Map<Integer, ExecutableElement> eventResponseMap = new HashMap<Integer, ExecutableElement>();

    private Messager messager;
    private Filer filer;
    private Elements elementUtils;

    private Template cppHeaderTemplate;
    private Template cppTemplate;
    private Template cppMessageTypeHeaderTemplate;

    private int round;

    @Override
    @SuppressWarnings("checkstyle:npathcomplexity")
    public void init(ProcessingEnvironment env) {
        messager = env.getMessager();
        logMessage(Diagnostic.Kind.NOTE, "Initializing code generator");

        filer = env.getFiler();
        elementUtils = env.getElementUtils();
        try {
            Logger.selectLoggerLibrary(Logger.LIBRARY_NONE);
        } catch (ClassNotFoundException e) {
            logMessage(Diagnostic.Kind.ERROR, e.getMessage());
        }
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_23);
        cfg.setTemplateLoader(new ClassTemplateLoader(getClass(), "/"));

        generateTests = Boolean.getBoolean(GENERATE_COMPATIBILITY_TESTS);

        for (Lang lang : Lang.values()) {
            getTemplates(cfg, lang);
        }
    }

    private void getTemplates(Configuration cfg, Lang lang) {
        boolean enabled = Boolean.getBoolean("hazelcast.generator." + lang.name().toLowerCase());
        if (enabled || lang == JAVA) {
            if (Lang.CPP == lang) {
                try {
                    cppHeaderTemplate = cfg.getTemplate("codec-template-" + lang.name().toLowerCase() + "header.ftl");
                } catch (IOException e) {
                    logMessage(Diagnostic.Kind.ERROR, "Cannot find cpp header template." + e.getMessage());
                }
                try {
                    cppTemplate = cfg.getTemplate("codec-template-" + lang.name().toLowerCase() + ".ftl");
                    codecTemplateMap.put(lang, cppTemplate);
                } catch (IOException e) {
                    logMessage(Diagnostic.Kind.ERROR, "Cannot find cpp template." + e.getMessage());
                }
                try {
                    cppMessageTypeHeaderTemplate = cfg.getTemplate("messagetype-template-" + lang.name().toLowerCase()
                            + "header.ftl");
                    messageTypeTemplateMap.put(lang, cppMessageTypeHeaderTemplate);
                } catch (IOException e) {
                    logMessage(Diagnostic.Kind.ERROR, "Cannot find cpp messagetype header template." + e.getMessage());
                }
            } else {
                try {
                    Template codecTemplate = cfg.getTemplate("codec-template-" + lang.name().toLowerCase() + ".ftl");
                    codecTemplateMap.put(lang, codecTemplate);
                } catch (IOException e) {
                    logMessage(Diagnostic.Kind.ERROR, "Cannot find template for lang:" + lang + ". " + e.getMessage());
                }
                try {
                    Template messageTypeTemplate = cfg.getTemplate("messagetype-template-" + lang.name().toLowerCase()
                            + ".ftl");
                    messageTypeTemplateMap.put(lang, messageTypeTemplate);
                } catch (IOException e) {
                    logMessage(Diagnostic.Kind.WARNING,
                            "Cannot find messagetype template for lang:" + lang + ". " + e.getMessage());
                }
            }

            if (generateTests) {
                getCompatibilityTestTemplates(cfg);
            }
        }
    }

    private void getCompatibilityTestTemplates(Configuration cfg) {
        for (CompatibilityTestInfo info :  compatibilityTestInfos) {
            try {
                info.setTemplate(cfg.getTemplate(info.getFileName() + ".ftl"));
            } catch (IOException e) {
                logMessage(Diagnostic.Kind.WARNING,
                        "Cannot find test template " + info.getFileName() + ".ftl" + ". " + e.getMessage());
            }
        }
    }

    private void logMessage(Diagnostic.Kind severityLevel, String message) {
        messager.printMessage(severityLevel, message);
        System.out.println(message);
    }

    @Override
    public boolean process(Set<? extends TypeElement> elements, RoundEnvironment env) {
        logMessage(Diagnostic.Kind.NOTE, "Processing code generator. round: " + (++round));
        try {
            //PREPARE META DATA
            for (Element element : env.getElementsAnnotatedWith(Codec.class)) {
                if (processElement(element)) {
                    continue;
                }
            }
            for (Element element : env.getElementsAnnotatedWith(GenerateCodec.class)) {
                register((TypeElement) element);
            }
            //END

            for (Lang lang : codecTemplateMap.keySet()) {
                generateContent(lang);
            }
        } catch (Exception e) {
            logMessage(Diagnostic.Kind.ERROR, e.getMessage());
            e.printStackTrace();
        }
        requestMap.clear();
        responseMap.clear();
        eventResponseMap.clear();
        return true;
    }

    private boolean processElement(Element element) {
        logMessage(Diagnostic.Kind.NOTE, "Processing element:" + element.toString());
        if (!(element instanceof TypeElement)) {
            logMessage(Diagnostic.Kind.WARNING,
                    "Skipping processing element:" + element.toString() + " annotated with @Codec.class is not a class.");
            return true;
        }
        TypeElement classElement = (TypeElement) element;
        Codec annotation = classElement.getAnnotation(Codec.class);
        if (annotation != null) {
            try {
                annotation.value();
            } catch (MirroredTypeException mte) {
                TypeMirror value = mte.getTypeMirror();
                CodecModel.CUSTOM_CODEC_MAP.put(value.toString(), classElement);
            }
        }
        return false;
    }

    void generateContent(Lang lang) {
        //GENERATE CONTENT
        Map<TypeElement, Map<Integer, CodecModel>> allCodecModel = createAllCodecModel(lang);

        if (allCodecModel.isEmpty()) {
            return;
        }

        Template messageTypeTemplate = messageTypeTemplateMap.get(lang);
        if (messageTypeTemplate != null) {
            for (Element element : allCodecModel.keySet()) {
                generateMessageTypeEnum((TypeElement) element, lang, messageTypeTemplate);
            }
        }

        Template codecTemplate = codecTemplateMap.get(lang);

        if (lang == Lang.MD) {
            generateDoc(allCodecModel, codecTemplate);
        } else if (lang == Lang.CPP) {
            generateContentForCpp(allCodecModel);
        } else {
            for (Map<Integer, CodecModel> map : allCodecModel.values()) {
                for (CodecModel model : map.values()) {
                    generateCodec(model, codecTemplate);
                }
            }

            if (Lang.JAVA == lang && generateTests) {
                generateCompatibilityTests(allCodecModel);
            }
        }
    }

    private void generateContentForCpp(Map<TypeElement, Map<Integer, CodecModel>> allCodecModel) {
        for (Map<Integer, CodecModel> map : allCodecModel.values()) {
            for (CodecModel model : map.values()) {
                if (CodeGenerationUtils.shouldGenerateForCpp(model.getParentName())) {
                    String content = generateFromTemplate(cppHeaderTemplate, model);
                    saveFile(model.getClassName() + ".h", "include." + model.getPackageName().toLowerCase(), content);
                    content = generateFromTemplate(cppTemplate, model);
                    saveFile(model.getClassName() + ".cpp", "src." + model.getPackageName().toLowerCase(), content);
                }
            }
        }
    }

    private void generateCompatibilityTests(Map<TypeElement, Map<Integer, CodecModel>> allCodecModel) {
        for (CompatibilityTestInfo info : compatibilityTestInfos) {
            if (null != info.template) {
                if (info.isVersioned()) {
                    for (int version : protocolVersions) {
                        String content = generateFromTemplate(info.template, allCodecModel, version);
                        saveClass(COMPATIBILITY_TEST_PACKAGE,
                                info.getFileName() + "_" + CodeGenerationUtils.versionAsClassName(version), content);
                    }
                } else {
                    String content = generateFromTemplate(info.template, allCodecModel,
                            protocolVersions[protocolVersions.length - 1]);
                    saveClass(COMPATIBILITY_TEST_PACKAGE, info.getFileName(), content);
                }
            }
        }
    }

    void register(TypeElement classElement) {
        HashMap<Integer, ExecutableElement> map = new HashMap<Integer, ExecutableElement>();
        requestMap.put(classElement, map);
        for (Element enclosedElement : classElement.getEnclosedElements()) {
            if (!enclosedElement.getKind().equals(ElementKind.METHOD)) {
                continue;
            }
            ExecutableElement methodElement = (ExecutableElement) enclosedElement;

            short masterId = classElement.getAnnotation(GenerateCodec.class).id();

            Request request = methodElement.getAnnotation(Request.class);
            if (request != null) {
                Integer id = Integer.parseInt(CodeGenerationUtils.mergeIds(masterId, request.id()), HEX_RADIX);
                map.put(id, methodElement);
                continue;
            }

            Response response = methodElement.getAnnotation(Response.class);
            if (response != null) {
                responseMap.put(response.value(), methodElement);
                continue;
            }

            EventResponse eventResponse = methodElement.getAnnotation(EventResponse.class);
            if (eventResponse != null) {
                eventResponseMap.put(eventResponse.value(), methodElement);
            }
        }
    }

    private Map<TypeElement, Map<Integer, CodecModel>> createAllCodecModel(Lang lang) {
        Map<TypeElement, Map<Integer, CodecModel>> model
                = new TreeMap<TypeElement, Map<Integer, CodecModel>>(new DistributedObjectComparator());

        for (Map.Entry<TypeElement, Map<Integer, ExecutableElement>> entry : requestMap.entrySet()) {
            Map<Integer, CodecModel> map = new TreeMap<Integer, CodecModel>();
            TypeElement parent = entry.getKey();
            model.put(parent, map);

            Map<Integer, ExecutableElement> operationMap = entry.getValue();
            for (Map.Entry<Integer, ExecutableElement> entrySub : operationMap.entrySet()) {
                ExecutableElement methodElement = entrySub.getValue();
                CodecModel codecModel = createCodecModel(methodElement, lang);
                String docComment = elementUtils.getDocComment(methodElement);
                if (null != docComment) {
                    codecModel.setComment(docComment);
                }
                map.put(entrySub.getKey(), codecModel);
            }
        }
        return model;
    }

    private CodecModel createCodecModel(ExecutableElement methodElement, Lang lang) {
        TypeElement parent = (TypeElement) methodElement.getEnclosingElement();

        Request methodElementAnnotation = methodElement.getAnnotation(Request.class);
        int response = methodElementAnnotation.response();
        int[] events = null;
        try {
            events = methodElementAnnotation.event();
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println(parent.toString());
            System.err.println(methodElement.toString());
        }
        boolean retryable = methodElementAnnotation.retryable();

        ExecutableElement responseElement = responseMap.get(response);

        List<ExecutableElement> eventElementList = new ArrayList<ExecutableElement>();
        if (events != null) {
            for (Integer eventType : events) {
                ExecutableElement eventResponse = eventResponseMap.get(eventType);
                if (eventResponse != null) {
                    eventElementList.add(eventResponse);
                }
            }
        }
        return new CodecModel(parent, methodElement, responseElement, eventElementList, retryable, lang, elementUtils);
    }

    public void generateCodec(CodecModel codecModel, Template codecTemplate) {
        final String content = generateFromTemplate(codecTemplate, codecModel);
        String fileName = codecModel.getClassName() + "." + codecModel.getLang().name().toLowerCase();

        switch (codecModel.getLang()) {
            case JAVA:
                saveClass(codecModel.getPackageName(), codecModel.getClassName(), content);
                break;
            case NODE:
                fileName = codecModel.getClassName() + ".ts";
                saveFile(fileName, codecModel.getPackageName(), content);
                break;
            case PY:
                fileName = fileName.replaceAll("(.)(\\p{Upper})", "$1_$2").toLowerCase();
                saveFile(fileName, codecModel.getPackageName(), content);
                break;
            default:
                saveFile(fileName, codecModel.getPackageName(), content);
                break;
        }
    }

    void generateDoc(Map<TypeElement, Map<Integer, CodecModel>> model, Template codecTemplate) {
        String content = generateFromTemplate(codecTemplate, model);
        String fileName = "HazelcastOpenBinaryProtocol-" + getClass().getPackage().getImplementationVersion();
        saveFile(fileName, "document", content);
    }

    private void generateMessageTypeEnum(TypeElement classElement, Lang lang, Template messageTypeTemplate) {
        MessageTypeEnumModel model = new MessageTypeEnumModel(classElement, lang);
        if (model.isEmpty()) {
            return;
        }

        if (Lang.CPP == lang) {
            if (CodeGenerationUtils.shouldGenerateForCpp(model.getName())) {
                String content = generateFromTemplate(cppMessageTypeHeaderTemplate, model);
                saveFile(model.getClassName() + ".h", "include." + model.getPackageName().toLowerCase(), content);
            }
        } else {
            String content = generateFromTemplate(messageTypeTemplate, model);
            saveContent(model, content);
        }
    }

    private String generateFromTemplate(Template template, Object model) {
        return generateFromTemplate(template, model, -1);
    }

    private String generateFromTemplate(Template template, Object model, int testForVersion) {
        String content = null;
        try {
            Map<String, Object> data = new HashMap<String, Object>();
            setUtilModel(data);
            data.put("model", model);
            data.put("testForVersion", testForVersion);
            StringWriter writer = new StringWriter();
            template.process(data, writer);
            content = writer.toString();
        } catch (Exception e) {
            logMessage(Diagnostic.Kind.ERROR, e.getMessage());
            e.printStackTrace();
        }
        return content;
    }

    private void saveContent(Model codecModel, String content) {
        if (codecModel.getLang() == JAVA) {
            saveClass(codecModel.getPackageName(), codecModel.getClassName(), content);
        } else {
            String fileName = codecModel.getClassName() + "." + codecModel.getLang().name().toLowerCase();
            if (codecModel.getLang() == Lang.PY) {
                fileName = fileName.replaceAll("(.)(\\p{Upper})", "$1_$2").toLowerCase();
            } else if (codecModel.getLang() == Lang.NODE) {
                fileName = codecModel.getClassName() + ".ts";
            }
            saveFile(fileName, codecModel.getPackageName(), content);
        }
    }

    private void saveClass(String packageName, String className, String content) {
        JavaFileObject file;
        try {
            String fullClassName = packageName + "." + className;
            file = filer.createSourceFile(fullClassName);
            file.openWriter().append(content).close();
        } catch (IOException e) {
            logMessage(Diagnostic.Kind.WARNING, e.getMessage());
            e.printStackTrace();
        }
    }

    private void saveFile(String fileName, String packageName, String content) {
        try {
            JavaFileManager.Location location = StandardLocation.locationFor(StandardLocation.SOURCE_OUTPUT.name());
            Writer writer = filer.createResource(location, packageName, fileName).openWriter();
            writer.append(content).close();
        } catch (IOException e) {
            logMessage(Diagnostic.Kind.WARNING, e.getMessage());
            e.printStackTrace();
        }
    }

    public static void setUtilModel(Map<String, Object> modelMap) throws TemplateModelException {
        BeansWrapper wrapper = BeansWrapper.getDefaultInstance();
        TemplateHashModel staticModels = wrapper.getStaticModels();
        TemplateHashModel statics = (TemplateHashModel) staticModels.get(CodeGenerationUtils.class.getName());
        modelMap.put("util", statics);
    }

    private static class DistributedObjectComparator implements Comparator<TypeElement>, Serializable {

        @Override
        public int compare(TypeElement o1, TypeElement o2) {
            GenerateCodec annotationForKey1 = o1.getAnnotation(GenerateCodec.class);
            GenerateCodec annotationForKey2 = o2.getAnnotation(GenerateCodec.class);
            if (annotationForKey1.id() == annotationForKey2.id()) {
                return annotationForKey1.name().compareTo(annotationForKey2.name());
            } else {
                return annotationForKey1.id() - annotationForKey2.id();
            }
        }
    }
}
