 package ${model.packageName};

import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.util.ParameterUtil;
import com.hazelcast.nio.Bits;

/**
 * @since ${model.messageSince}
 * update ${util.versionAsString(model.highestParameterVersion)}
 */
@edu.umd.cs.findbugs.annotations.SuppressFBWarnings({"URF_UNREAD_PUBLIC_OR_PROTECTED_FIELD"})
public final class ${model.className} {

    public static final ${model.parentName}MessageType REQUEST_TYPE = ${model.parentName}MessageType.${model.parentName?upper_case}_${model.name?upper_case};
    public static final int RESPONSE_TYPE = ${model.response};

    //************************ REQUEST *************************//

    public static class RequestParameters {
    public static final ${model.parentName}MessageType TYPE = REQUEST_TYPE;

         /**
         * @since ${model.messageSince}
         */
    <#list model.requestParams as param>
        <#assign messageVersion=model.messageSinceInt>
        <#if param.sinceVersionInt gt messageVersion >
         /**
         * @since ${param.sinceVersion}
         */
        public boolean ${param.name}Exist = false;
        </#if>
        public ${param.type} ${param.name};
    </#list>

    <#list model.versionedRequestParams as version, requestParams>
         /**
         * @since ${version}
         */
        public static int calculateDataSize(<#list requestParams as param>${methodParam(param.type)} ${param.name}<#if param_has_next>, </#if></#list>) {
            int dataSize = ClientMessage.HEADER_SIZE;
            <#list requestParams as p>
            <@sizeText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
            </#list>
            return dataSize;
        }
    </#list>
    }

    <#list model.versionedRequestParams as version, requestParams>
         /**
         * @since ${version}
         */
        public static ClientMessage encodeRequest(<#list requestParams as param>${methodParam(param.type)} ${param.name}<#if param_has_next>, </#if></#list>) {
            final int requiredDataSize = RequestParameters.calculateDataSize(<#list requestParams as param>${param.name}<#if param_has_next>, </#if></#list>);
            ClientMessage clientMessage = ClientMessage.createForEncode(requiredDataSize);
            clientMessage.setMessageType(REQUEST_TYPE.id());
            clientMessage.setRetryable(<#if model.retryable == 1>true<#else>false</#if>);
            clientMessage.setAcquiresResource(<#if model.acquiresResource == 1>true<#else>false</#if>);
            clientMessage.setOperationName("${model.parentName}.${model.name}");
            <#list requestParams as p>
            <@setterText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
            </#list>
            clientMessage.updateFrameLength();
            return clientMessage;
        }
    </#list>

    public static RequestParameters decodeRequest(ClientMessage clientMessage) {
        final RequestParameters parameters = new RequestParameters();
<#list model.requestParams as p>
    <#if p.versionChanged >
        if (clientMessage.isComplete()) {
            return parameters;
        }
    </#if>
    <#--  Id 2: AuthenticationCodec, Id:3 CustomAuthenticationCodec -->
    <#if p.name == "clientHazelcastVersion" && (model.id == "0x0002" || model.id == "0x0003") >
            try {
            <@getterText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
            } catch (IndexOutOfBoundsException e) {
                if ("CSP".equals(parameters.clientType)) {
                    // suppress this error for older csharp client since they had a bug which was fixed later (writeByte related)
                    return parameters;
                } else {
                    throw e;
                }
            }
    <#else>
           <@getterText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
    </#if>
    <#if p.sinceVersionInt gt messageVersion >parameters.${p.name}Exist = true;</#if>
</#list>
        return parameters;
    }

    //************************ RESPONSE *************************//

    public static class ResponseParameters {
         /**
         * @since ${model.messageSince}
         */
<#list model.responseParams as param>
        <#assign messageVersion=model.messageSinceInt>
        <#if param.sinceVersionInt gt messageVersion >
         /**
         * @since ${param.sinceVersion}
         */
        public boolean ${param.name}Exist = false;
        </#if>
        public ${param.type} ${param.name};
</#list>

    <#list model.versionedResponseParams as version, responseParams>
         /**
         * @since ${version}
         */
        public static int calculateDataSize(<#list responseParams as param> ${methodParam(param.type)} ${param.name}<#if param_has_next>, </#if></#list>) {
            int dataSize = ClientMessage.HEADER_SIZE;
            <#list responseParams as p>
            <@sizeText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
            </#list>
            return dataSize;
        }
    </#list>
    }

<#list model.versionedResponseParams as version, responseParams>
    /**
    * @since ${version}
    */
    public static ClientMessage encodeResponse(<#list responseParams as param>${methodParam(param.type)} ${param.name}<#if param_has_next>, </#if></#list>) {
        final int requiredDataSize = ResponseParameters.calculateDataSize(<#list responseParams as param>${param.name}<#if param_has_next>, </#if></#list>);
        ClientMessage clientMessage = ClientMessage.createForEncode(requiredDataSize);
        clientMessage.setMessageType(RESPONSE_TYPE);
<#list responseParams as p>
    <@setterText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
</#list>
        clientMessage.updateFrameLength();
        return clientMessage;

    }
</#list>

    public static ResponseParameters decodeResponse(ClientMessage clientMessage) {
        ResponseParameters parameters = new ResponseParameters();
<#list model.responseParams as p>
    <#if p.versionChanged >
        if (clientMessage.isComplete()) {
            return parameters;
        }
    </#if>
    <@getterText var_name=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
    <#if p.sinceVersionInt gt messageVersion >parameters.${p.name}Exist = true;</#if>
</#list>
        return parameters;
    }

<#if model.events?has_content>

    //************************ EVENTS *************************//

<#list model.events as event>
    public static ClientMessage encode${event.name}Event(<#list event.eventParams as param>${methodParam(param.type)} ${param.name}<#if param_has_next>, </#if></#list>){
        int dataSize = ClientMessage.HEADER_SIZE;
    <#list event.eventParams as p>
        <@sizeText var_name=p.name type=p.type isNullable=p.nullable/>
    </#list>;

        ClientMessage clientMessage = ClientMessage.createForEncode(dataSize);
        clientMessage.setMessageType(com.hazelcast.client.impl.protocol.constants.EventMessageConst.EVENT_${event.name?upper_case});
        clientMessage.addFlag(ClientMessage.LISTENER_EVENT_FLAG);

    <#list event.eventParams as p>
        <@setterText var_name=p.name type=p.type isNullable=p.nullable/>
    </#list>
        clientMessage.updateFrameLength();
        return clientMessage;
    };

</#list>

  public static abstract class AbstractEventHandler{

        public void handle(ClientMessage clientMessage) {
            int messageType = clientMessage.getMessageType();
        <#list model.events as event>
            if (messageType == com.hazelcast.client.impl.protocol.constants.EventMessageConst.EVENT_${event.name?upper_case}) {
            <#assign paramCallList="">
            <#assign previousVersion = event.sinceVersion?replace('.','') >
            <#list event.eventParams as p>
                <#if p.versionChanged >
                    if (clientMessage.isComplete()) {
                        handle${event.name?cap_first}EventV${previousVersion}(${paramCallList});
                        return;
                    }
                </#if>
                <#if p_index gt 0 ><#assign paramCallList=paramCallList + ", "></#if>
                <#assign paramCallList+=p.name>
                <#assign previousVersion = p.sinceVersion?replace('.','') >
                <@defineVariable var_name=p.name type=p.type />
                <@readVariable var_name=p.name type=p.type isNullable=p.nullable isEvent=true />
            </#list>
                handle${event.name?cap_first}EventV${previousVersion}(${paramCallList});
                return;
            }
        </#list>
            com.hazelcast.logging.Logger.getLogger(super.getClass()).warning("Unknown message type received on event handler :" + messageType);
        }

    <#list model.events as event>
        <#list event.versionedEventParams as sinceVersion, eventParams>
            <#assign version = sinceVersion?replace('.','') >
            public abstract void handle${event.name?cap_first}EventV${version}(<#list eventParams as param>${methodParam(param.type)} ${param.name}<#if param_has_next>, </#if></#list>);
        </#list>
    </#list>
   }

</#if>
}
<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText var_name type isNullable=false containsNullable=false>
<#if isNullable>
            dataSize += Bits.BOOLEAN_SIZE_IN_BYTES;
            if (${var_name} != null) {
</#if>
<@sizeTextInternal var_name=var_name type=type containsNullable=containsNullable/>
<#if isNullable>
            }
</#if>
</#macro>


<#--METHOD PARAM Function -->
<#function methodParam type><#local cat= util.getTypeCategory(type)>
    <#switch cat>
        <#case "COLLECTION">
            <#local genericType= util.getGenericType(type)>
            <#return "java.util.Collection<${genericType}>">
            <#break>
        <#default>
            <#return "${type}">
    </#switch>
</#function>

<#--SIZE MACRO -->
<#macro sizeTextInternal var_name type containsNullable=false>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
    <#case "OTHER">
        <#if util.isPrimitive(type)>
            dataSize += Bits.${type?upper_case}_SIZE_IN_BYTES;
        <#else >
            dataSize += ParameterUtil.calculateDataSize(${var_name});
        </#if>
        <#break >
    <#case "CUSTOM">
            dataSize += ${util.getTypeCodec(type)}.calculateDataSize(${var_name});
        <#break >
    <#case "COLLECTION">
            dataSize += Bits.INT_SIZE_IN_BYTES;
        <#local genericType= util.getGenericType(type)>
        <#local n= var_name>
            for (${genericType} ${var_name}_item : ${var_name} ) {
        <@sizeText var_name="${n}_item"  type=genericType isNullable=containsNullable/>
            }
        <#break >
    <#case "ARRAY">
            dataSize += Bits.INT_SIZE_IN_BYTES;
        <#local genericType= util.getArrayType(type)>
        <#local n= var_name>
            for (${genericType} ${var_name}_item : ${var_name} ) {
        <@sizeText var_name="${n}_item"  type=genericType isNullable=containsNullable/>
            }
        <#break >
    <#case "MAPENTRY">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
        <#local n= var_name>
        <#local keyName="${var_name}Key">
        <#local valName="${var_name}Val">
            ${keyType} ${keyName} =  ${var_name}.getKey();
            ${valueType} ${valName} =  ${var_name}.getValue();
        <@sizeText var_name="${keyName}"  type=keyType/>
        <@sizeText var_name="${valName}"  type=valueType/>
</#switch>
</#macro>

<#--SETTER NULL CHECK MACRO -->
<#macro setterText var_name type isNullable=false containsNullable=false>
<#local isNullVariableName= "${var_name}_isNull">
<#if isNullable>
        boolean ${isNullVariableName};
        if (${var_name} == null) {
            ${isNullVariableName} = true;
            clientMessage.set(${isNullVariableName});
        } else {
            ${isNullVariableName}= false;
            clientMessage.set(${isNullVariableName});
</#if>
<@setterTextInternal var_name=var_name type=type containsNullable=containsNullable/>
<#if isNullable>
        }
</#if>
</#macro>

<#--SETTER MACRO -->
<#macro setterTextInternal var_name type isNullable=false containsNullable=false>
    <#local cat= util.getTypeCategory(type)>
    <#if cat == "OTHER">
        clientMessage.set(${var_name});
    </#if>
    <#if cat == "CUSTOM">
        ${util.getTypeCodec(type)}.encode(${var_name}, clientMessage);
    </#if>
    <#if cat == "COLLECTION">
        clientMessage.set(${var_name}.size());
        <#local itemType= util.getGenericType(type)>
        <#local itemTypeVar= var_name + "_item">
        for (${itemType} ${itemTypeVar} : ${var_name}) {
        <@setterText var_name=itemTypeVar type=itemType isNullable=containsNullable/>
        }
    </#if>
    <#if cat == "ARRAY">
        clientMessage.set(${var_name}.length);
        <#local itemType= util.getArrayType(type)>
        <#local itemTypeVar= var_name + "_item">
        for (${itemType} ${itemTypeVar} : ${var_name}) {
        <@setterText var_name=itemTypeVar  type=itemType isNullable=containsNullable/>
        }
    </#if>
    <#if cat == "MAPENTRY">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
        <#local keyName="${var_name}Key">
        <#local valName="${var_name}Val">
            ${keyType} ${keyName} = ${var_name}.getKey();
            ${valueType} ${valName} = ${var_name}.getValue();
        <@setterTextInternal var_name="${keyName}"  type=keyType/>
        <@setterTextInternal var_name="${valName}"  type=valueType/>
    </#if>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText var_name type isNullable=false isEvent=false containsNullable=false>
        <@defineVariable var_name=var_name type=type />
        <@readVariable var_name=var_name type=type isNullable=isNullable isEvent=isEvent containsNullable=containsNullable />
</#macro>

<#-- Only defines the variable -->
<#macro defineVariable var_name type >
        ${type} ${var_name} = <@getDefaultValueForType type=type />;
</#macro>

<#-- Reads the variable from client message -->
<#macro readVariable var_name type isNullable isEvent containsNullable=false>
<#local isNullVariableName= "${var_name}_isNull">
<#if isNullable>
        boolean ${isNullVariableName} = clientMessage.getBoolean();
        if (!${isNullVariableName}) {
</#if>
<@getterTextInternal var_name=var_name varType=type containsNullable=containsNullable/>
<#if !isEvent>
            parameters.${var_name} = ${var_name};
</#if>
<#if isNullable>
        }
</#if>
</#macro>

<#macro getterTextInternal var_name varType containsNullable=false>
<#local cat= util.getTypeCategory(varType)>
<#switch cat>
    <#case "OTHER">
        <#switch varType>
            <#case util.DATA_FULL_NAME>
        ${var_name} = clientMessage.getData();
                <#break >
            <#case "java.lang.Integer">
        ${var_name} = clientMessage.getInt();
                <#break >
            <#case "java.lang.Long">
        ${var_name} = clientMessage.getLong();
                <#break >
            <#case "java.lang.Boolean">
        ${var_name} = clientMessage.getBoolean();
                <#break >
            <#case "java.lang.String">
        ${var_name} = clientMessage.getStringUtf8();
                <#break >
            <#default>
        ${var_name} = clientMessage.get${util.capitalizeFirstLetter(varType)}();
        </#switch>
        <#break >
    <#case "CUSTOM">
            ${var_name} = ${util.getTypeCodec(varType)}.decode(clientMessage);
        <#break >
    <#case "COLLECTION">
    <#local collectionType>java.util.ArrayList</#local>
    <#local itemVariableType= util.getGenericType(varType)>
    <#local itemVariableName= "${var_name}_item">
    <#local sizeVariableName= "${var_name}_size">
    <#local indexVariableName= "${var_name}_index">
    <#local isNullVariableName= "${itemVariableName}_isNull">
            int ${sizeVariableName} = clientMessage.getInt();
            ${var_name} = new ${collectionType}<${itemVariableType}>(${sizeVariableName});
            for (int ${indexVariableName} = 0;${indexVariableName}<${sizeVariableName};${indexVariableName}++) {
                ${itemVariableType} ${itemVariableName};
                <#if containsNullable>
                        ${itemVariableName} = null;
                        boolean ${isNullVariableName} = clientMessage.getBoolean();
                        if (!${isNullVariableName}) {
                </#if>
                <@getterTextInternal var_name=itemVariableName varType=itemVariableType/>
                <#if containsNullable>
                        }
                </#if>
                ${var_name}.add(${itemVariableName});
            }
        <#break >
    <#case "ARRAY">
    <#local itemVariableType= util.getArrayType(varType)>
    <#local itemVariableName= "${var_name}_item">
    <#local sizeVariableName= "${var_name}_size">
    <#local indexVariableName= "${var_name}_index">
    <#local isNullVariableName= "${itemVariableName}_isNull">
            int ${sizeVariableName} = clientMessage.getInt();
            ${var_name} = new ${itemVariableType}[${sizeVariableName}];
            for (int ${indexVariableName} = 0;${indexVariableName}<${sizeVariableName};${indexVariableName}++) {
                ${itemVariableType} ${itemVariableName};
                <#if containsNullable>
                        ${itemVariableName} = null;
                        boolean ${isNullVariableName} = clientMessage.getBoolean();
                        if (!${isNullVariableName}) {
                </#if>
                <@getterTextInternal var_name=itemVariableName varType=itemVariableType/>
                <#if containsNullable>
                        }
                </#if>
                ${var_name}[${indexVariableName}] = ${itemVariableName};
            }
        <#break >
    <#case "MAPENTRY">
        <#local sizeVariableName= "${var_name}_size">
        <#local indexVariableName= "${var_name}_index">
        <#local keyType = util.getFirstGenericParameterType(varType)>
        <#local valueType = util.getSecondGenericParameterType(varType)>
        <#local keyVariableName= "${var_name}_key">
        <#local valVariableName= "${var_name}_val">
            ${keyType} ${keyVariableName};
            ${valueType} ${valVariableName};
            <@getterTextInternal var_name=keyVariableName varType=keyType/>
            <@getterTextInternal var_name=valVariableName varType=valueType/>
        ${var_name} = new java.util.AbstractMap.SimpleEntry<${keyType},${valueType}>(${keyVariableName}, ${valVariableName});
</#switch>
</#macro>

<#--Gets the default value for a type in java -->
<#macro getDefaultValueForType type>
<#if type == "boolean" >
false
<#elseif util.isPrimitive(type) >
0
<#else>
null
</#if>
</#macro>
