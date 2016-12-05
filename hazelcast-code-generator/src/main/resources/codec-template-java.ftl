package ${model.packageName};

import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.util.ParameterUtil;
import com.hazelcast.nio.Bits;
import javax.annotation.Generated;

@Generated("Hazelcast.code.generator")
@edu.umd.cs.findbugs.annotations.SuppressFBWarnings({"URF_UNREAD_PUBLIC_OR_PROTECTED_FIELD"})
public final class ${model.className} {

    public static final ${model.parentName}MessageType REQUEST_TYPE = ${model.parentName}MessageType.${model.parentName?upper_case}_${model.name?upper_case};
    public static final int RESPONSE_TYPE = ${model.response};
    public static final boolean RETRYABLE = <#if model.retryable == 1>true<#else>false</#if>;

    //************************ REQUEST *************************//

    public static class RequestParameters {
    public static final ${model.parentName}MessageType TYPE = REQUEST_TYPE;
<#list model.requestParams as param>
<#assign messageVersion=model.messageSinceInt>
        public ${param.type} ${param.name};
        <#if param.sinceVersionInt gt messageVersion >public boolean ${param.name}Exist = false;</#if>
</#list>

        public static int calculateDataSize(<#list model.requestParams as param><@methodParam type=param.type/> ${param.name}<#if param_has_next>, </#if></#list>) {
            int dataSize = ClientMessage.HEADER_SIZE;
<#list model.requestParams as p>
    <@sizeText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
</#list>
            return dataSize;
        }
    }

    public static ClientMessage encodeRequest(<#list model.requestParams as param><@methodParam type=param.type/> ${param.name}<#if param_has_next>, </#if></#list>) {
        final int requiredDataSize = RequestParameters.calculateDataSize(<#list model.requestParams as param>${param.name}<#if param_has_next>, </#if></#list>);
        ClientMessage clientMessage = ClientMessage.createForEncode(requiredDataSize);
        clientMessage.setMessageType(REQUEST_TYPE.id());
        clientMessage.setRetryable(RETRYABLE);
<#list model.requestParams as p>
    <@setterText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
</#list>
        clientMessage.updateFrameLength();
        return clientMessage;
    }

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
            <@getterText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
            } catch (IndexOutOfBoundsException e) {
                if (parameters.clientType == "CSHARP") {
                    // suppress this error for older csharp client since they had a bug which was fixed later (writeByte related)
                    return parameters;
                } else {
                    throw e;
                }
            }
    <#else>
           <@getterText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
    </#if>
    <#if p.sinceVersionInt gt messageVersion >parameters.${p.name}Exist = true;</#if>
</#list>
        return parameters;
    }

    //************************ RESPONSE *************************//

    public static class ResponseParameters {
<#list model.responseParams as param>
        public ${param.type} ${param.name};
<#assign messageVersion=model.messageSinceInt>
        <#if param.sinceVersionInt gt messageVersion >public boolean ${param.name}Exist = false;</#if>
</#list>

        public static int calculateDataSize(<#list model.responseParams as param><@methodParam type=param.type/> ${param.name}<#if param_has_next>, </#if></#list>) {
            int dataSize = ClientMessage.HEADER_SIZE;
<#list model.responseParams as p>
    <@sizeText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
</#list>
            return dataSize;
        }
    }

    public static ClientMessage encodeResponse(<#list model.responseParams as param><@methodParam type=param.type/> ${param.name}<#if param_has_next>, </#if></#list>) {
        final int requiredDataSize = ResponseParameters.calculateDataSize(<#list model.responseParams as param>${param.name}<#if param_has_next>, </#if></#list>);
        ClientMessage clientMessage = ClientMessage.createForEncode(requiredDataSize);
        clientMessage.setMessageType(RESPONSE_TYPE);
<#list model.responseParams as p>
    <@setterText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
</#list>
        clientMessage.updateFrameLength();
        return clientMessage;

    }

    public static ResponseParameters decodeResponse(ClientMessage clientMessage) {
        ResponseParameters parameters = new ResponseParameters();
<#list model.responseParams as p>
    <#if p.versionChanged >
        if (clientMessage.isComplete()) {
            return parameters;
        }
    </#if>
    <@getterText varName=p.name type=p.type isNullable=p.nullable containsNullable=p.containsNullable/>
    <#if p.sinceVersionInt gt messageVersion >parameters.${p.name}Exist = true;</#if>
</#list>
        return parameters;
    }

<#if model.events?has_content>

    //************************ EVENTS *************************//

<#list model.events as event>
    public static ClientMessage encode${event.name}Event(<#list event.eventParams as param><@methodParam type=param.type/> ${param.name}<#if param_has_next>, </#if></#list>){
        int dataSize = ClientMessage.HEADER_SIZE;
    <#list event.eventParams as p>
        <@sizeText varName=p.name type=p.type isNullable=p.nullable/>
    </#list>;

        ClientMessage clientMessage = ClientMessage.createForEncode(dataSize);
        clientMessage.setMessageType(com.hazelcast.client.impl.protocol.constants.EventMessageConst.EVENT_${event.name?upper_case});
        clientMessage.addFlag(ClientMessage.LISTENER_EVENT_FLAG);

    <#list event.eventParams as p>
        <@setterText varName=p.name type=p.type isNullable=p.nullable/>
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
            boolean messageFinished = false;
            <#list event.eventParams as p>
                <@defineVariable varName=p.name type=p.type />
                <#if p.versionChanged >
                    if (!messageFinished) {
                        messageFinished = clientMessage.isComplete();
                    }
                </#if>
                    if (!messageFinished) {
                        <@readVariable varName=p.name type=p.type isNullable=p.nullable isEvent=true />
                    }
            </#list>
                handle(<#list event.eventParams as param>${param.name}<#if param_has_next>, </#if></#list>);
                return;
            }
        </#list>
            com.hazelcast.logging.Logger.getLogger(super.getClass()).warning("Unknown message type received on event handler :" + clientMessage.getMessageType());
        }

    <#list model.events as event>
        public abstract void handle(<#list event.eventParams as param><@methodParam type=param.type/> ${param.name}<#if param_has_next>, </#if></#list>);

    </#list>
   }

</#if>
}
<#--MACROS BELOW-->
<#--SIZE NULL CHECK MACRO -->
<#macro sizeText varName type isNullable=false containsNullable=false>
<#if isNullable>
            dataSize += Bits.BOOLEAN_SIZE_IN_BYTES;
            if (${varName} != null) {
</#if>
<@sizeTextInternal varName=varName type=type containsNullable=containsNullable/>
<#if isNullable>
            }
</#if>
</#macro>


<#--METHOD PARAM MACRO -->
<#macro methodParam type><#local cat= util.getTypeCategory(type)>
<#switch cat>
<#case "COLLECTION"><#local genericType= util.getGenericType(type)>java.util.Collection<${genericType}><#break>
<#default>${type}
</#switch>
</#macro>

<#--SIZE MACRO -->
<#macro sizeTextInternal varName type containsNullable=false>
<#local cat= util.getTypeCategory(type)>
<#switch cat>
    <#case "OTHER">
        <#if util.isPrimitive(type)>
            dataSize += Bits.${type?upper_case}_SIZE_IN_BYTES;
        <#else >
            dataSize += ParameterUtil.calculateDataSize(${varName});
        </#if>
        <#break >
    <#case "CUSTOM">
            dataSize += ${util.getTypeCodec(type)}.calculateDataSize(${varName});
        <#break >
    <#case "COLLECTION">
            dataSize += Bits.INT_SIZE_IN_BYTES;
        <#local genericType= util.getGenericType(type)>
        <#local n= varName>
            for (${genericType} ${varName}_item : ${varName} ) {
        <@sizeText varName="${n}_item"  type=genericType isNullable=containsNullable/>
            }
        <#break >
    <#case "ARRAY">
            dataSize += Bits.INT_SIZE_IN_BYTES;
        <#local genericType= util.getArrayType(type)>
        <#local n= varName>
            for (${genericType} ${varName}_item : ${varName} ) {
        <@sizeText varName="${n}_item"  type=genericType isNullable=containsNullable/>
            }
        <#break >
    <#case "MAPENTRY">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
        <#local n= varName>
            ${keyType} key =  ${varName}.getKey();
            ${valueType} val =  ${varName}.getValue();
        <@sizeText varName="key"  type=keyType/>
        <@sizeText varName="val"  type=valueType/>
</#switch>
</#macro>

<#--SETTER NULL CHECK MACRO -->
<#macro setterText varName type isNullable=false containsNullable=false>
<#local isNullVariableName= "${varName}_isNull">
<#if isNullable>
        boolean ${isNullVariableName};
        if (${varName} == null) {
            ${isNullVariableName} = true;
            clientMessage.set(${isNullVariableName});
        } else {
            ${isNullVariableName}= false;
            clientMessage.set(${isNullVariableName});
</#if>
<@setterTextInternal varName=varName type=type containsNullable=containsNullable/>
<#if isNullable>
        }
</#if>
</#macro>

<#--SETTER MACRO -->
<#macro setterTextInternal varName type isNullable=false containsNullable=false>
    <#local cat= util.getTypeCategory(type)>
    <#if cat == "OTHER">
        clientMessage.set(${varName});
    </#if>
    <#if cat == "CUSTOM">
        ${util.getTypeCodec(type)}.encode(${varName}, clientMessage);
    </#if>
    <#if cat == "COLLECTION">
        clientMessage.set(${varName}.size());
        <#local itemType= util.getGenericType(type)>
        <#local itemTypeVar= varName + "_item">
        for (${itemType} ${itemTypeVar} : ${varName}) {
        <@setterText varName=itemTypeVar type=itemType isNullable=containsNullable/>
        }
    </#if>
    <#if cat == "ARRAY">
        clientMessage.set(${varName}.length);
        <#local itemType= util.getArrayType(type)>
        <#local itemTypeVar= varName + "_item">
        for (${itemType} ${itemTypeVar} : ${varName}) {
        <@setterText varName=itemTypeVar  type=itemType isNullable=containsNullable/>
        }
    </#if>
    <#if cat == "MAPENTRY">
        <#local keyType = util.getFirstGenericParameterType(type)>
        <#local valueType = util.getSecondGenericParameterType(type)>
            ${keyType} key = ${varName}.getKey();
            ${valueType} val = ${varName}.getValue();
        <@setterTextInternal varName="key"  type=keyType/>
        <@setterTextInternal varName="val"  type=valueType/>
    </#if>
</#macro>

<#--GETTER NULL CHECK MACRO -->
<#macro getterText varName type isNullable=false isEvent=false containsNullable=false>
        <@defineVariable varName=varName type=type />
        <@readVariable varName=varName type=type isNullable=isNullable isEvent=isEvent containsNullable=containsNullable />
</#macro>

<#-- Only defines the variable -->
<#macro defineVariable varName type >
        ${type} ${varName} = <@getDefaultValueForType type=type />;
</#macro>

<#-- Reads the variable from client message -->
<#macro readVariable varName type isNullable isEvent containsNullable=false>
<#local isNullVariableName= "${varName}_isNull">
<#if isNullable>
        boolean ${isNullVariableName} = clientMessage.getBoolean();
        if (!${isNullVariableName}) {
</#if>
<@getterTextInternal varName=varName varType=type containsNullable=containsNullable/>
<#if !isEvent>
            parameters.${varName} = ${varName};
</#if>
<#if isNullable>
        }
</#if>
</#macro>

<#macro getterTextInternal varName varType containsNullable=false>
<#local cat= util.getTypeCategory(varType)>
<#switch cat>
    <#case "OTHER">
        <#switch varType>
            <#case util.DATA_FULL_NAME>
        ${varName} = clientMessage.getData();
                <#break >
            <#case "java.lang.Integer">
        ${varName} = clientMessage.getInt();
                <#break >
            <#case "java.lang.Long">
        ${varName} = clientMessage.getLong();
                <#break >
            <#case "java.lang.Boolean">
        ${varName} = clientMessage.getBoolean();
                <#break >
            <#case "java.lang.String">
        ${varName} = clientMessage.getStringUtf8();
                <#break >
            <#default>
        ${varName} = clientMessage.get${util.capitalizeFirstLetter(varType)}();
        </#switch>
        <#break >
    <#case "CUSTOM">
            ${varName} = ${util.getTypeCodec(varType)}.decode(clientMessage);
        <#break >
    <#case "COLLECTION">
    <#local collectionType>java.util.ArrayList</#local>
    <#local itemVariableType= util.getGenericType(varType)>
    <#local itemVariableName= "${varName}_item">
    <#local sizeVariableName= "${varName}_size">
    <#local indexVariableName= "${varName}_index">
    <#local isNullVariableName= "${itemVariableName}_isNull">
            int ${sizeVariableName} = clientMessage.getInt();
            ${varName} = new ${collectionType}<${itemVariableType}>(${sizeVariableName});
            for (int ${indexVariableName} = 0;${indexVariableName}<${sizeVariableName};${indexVariableName}++) {
                ${itemVariableType} ${itemVariableName} = null;
                <#if containsNullable>
                        boolean ${isNullVariableName} = clientMessage.getBoolean();
                        if (!${isNullVariableName}) {
                </#if>
                <@getterTextInternal varName=itemVariableName varType=itemVariableType/>
                <#if containsNullable>
                        }
                </#if>
                ${varName}.add(${itemVariableName});
            }
        <#break >
    <#case "ARRAY">
    <#local itemVariableType= util.getArrayType(varType)>
    <#local itemVariableName= "${varName}_item">
    <#local sizeVariableName= "${varName}_size">
    <#local indexVariableName= "${varName}_index">
    <#local isNullVariableName= "${itemVariableName}_isNull">
            int ${sizeVariableName} = clientMessage.getInt();
            ${varName} = new ${itemVariableType}[${sizeVariableName}];
            for (int ${indexVariableName} = 0;${indexVariableName}<${sizeVariableName};${indexVariableName}++) {
                ${itemVariableType} ${itemVariableName} = null;
                <#if containsNullable>
                        boolean ${isNullVariableName} = clientMessage.getBoolean();
                        if (!${isNullVariableName}) {
                </#if>
                <@getterTextInternal varName=itemVariableName varType=itemVariableType/>
                <#if containsNullable>
                        }
                </#if>
            }
        <#break >
    <#case "MAPENTRY">
        <#local sizeVariableName= "${varName}_size">
        <#local indexVariableName= "${varName}_index">
        <#local keyType = util.getFirstGenericParameterType(varType)>
        <#local valueType = util.getSecondGenericParameterType(varType)>
        <#local keyVariableName= "${varName}_key">
        <#local valVariableName= "${varName}_val">
            ${keyType} ${keyVariableName};
            ${valueType} ${valVariableName};
            <@getterTextInternal varName=keyVariableName varType=keyType/>
            <@getterTextInternal varName=valVariableName varType=valueType/>
        ${varName} = new java.util.AbstractMap.SimpleEntry<${keyType},${valueType}>(${keyVariableName}, ${valVariableName});
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