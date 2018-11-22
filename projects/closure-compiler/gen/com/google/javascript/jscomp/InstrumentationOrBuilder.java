// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: com/google/javascript/jscomp/instrumentation_template.proto

package com.google.javascript.jscomp;

public interface InstrumentationOrBuilder
    extends com.google.protobuf.MessageOrBuilder {

  // optional string report_defined = 1;
  /**
   * <code>optional string report_defined = 1;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;);
   * used to inform the harness about the contents of a module
   * </pre>
   */
  boolean hasReportDefined();
  /**
   * <code>optional string report_defined = 1;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;);
   * used to inform the harness about the contents of a module
   * </pre>
   */
  java.lang.String getReportDefined();
  /**
   * <code>optional string report_defined = 1;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;);
   * used to inform the harness about the contents of a module
   * </pre>
   */
  com.google.protobuf.ByteString
      getReportDefinedBytes();

  // optional string report_call = 2;
  /**
   * <code>optional string report_call = 2;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;);
   * used to inform the harness about a function call
   * </pre>
   */
  boolean hasReportCall();
  /**
   * <code>optional string report_call = 2;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;);
   * used to inform the harness about a function call
   * </pre>
   */
  java.lang.String getReportCall();
  /**
   * <code>optional string report_call = 2;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;);
   * used to inform the harness about a function call
   * </pre>
   */
  com.google.protobuf.ByteString
      getReportCallBytes();

  // optional string report_exit = 6;
  /**
   * <code>optional string report_exit = 6;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;, VAL = &lt;return value&gt;);
   * used to inform the harness about a function exit.  Must return
   * its second argument.
   *
   * @return VAL
   * </pre>
   */
  boolean hasReportExit();
  /**
   * <code>optional string report_exit = 6;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;, VAL = &lt;return value&gt;);
   * used to inform the harness about a function exit.  Must return
   * its second argument.
   *
   * @return VAL
   * </pre>
   */
  java.lang.String getReportExit();
  /**
   * <code>optional string report_exit = 6;</code>
   *
   * <pre>
   * name of function(ID = &lt;numeric function id&gt;, VAL = &lt;return value&gt;);
   * used to inform the harness about a function exit.  Must return
   * its second argument.
   *
   * @return VAL
   * </pre>
   */
  com.google.protobuf.ByteString
      getReportExitBytes();

  // repeated string declaration_to_remove = 3;
  /**
   * <code>repeated string declaration_to_remove = 3;</code>
   *
   * <pre>
   * List of variable declarations in the application's source code
   * that should be replaced by variables with the same name that are
   * part of the instrumentation harness.  The presence of these
   * declarations in the original code allows debug UIs that access
   * these variables to compile when the instrumentation pass is
   * disabled.
   * </pre>
   */
  java.util.List<java.lang.String>
  getDeclarationToRemoveList();
  /**
   * <code>repeated string declaration_to_remove = 3;</code>
   *
   * <pre>
   * List of variable declarations in the application's source code
   * that should be replaced by variables with the same name that are
   * part of the instrumentation harness.  The presence of these
   * declarations in the original code allows debug UIs that access
   * these variables to compile when the instrumentation pass is
   * disabled.
   * </pre>
   */
  int getDeclarationToRemoveCount();
  /**
   * <code>repeated string declaration_to_remove = 3;</code>
   *
   * <pre>
   * List of variable declarations in the application's source code
   * that should be replaced by variables with the same name that are
   * part of the instrumentation harness.  The presence of these
   * declarations in the original code allows debug UIs that access
   * these variables to compile when the instrumentation pass is
   * disabled.
   * </pre>
   */
  java.lang.String getDeclarationToRemove(int index);
  /**
   * <code>repeated string declaration_to_remove = 3;</code>
   *
   * <pre>
   * List of variable declarations in the application's source code
   * that should be replaced by variables with the same name that are
   * part of the instrumentation harness.  The presence of these
   * declarations in the original code allows debug UIs that access
   * these variables to compile when the instrumentation pass is
   * disabled.
   * </pre>
   */
  com.google.protobuf.ByteString
      getDeclarationToRemoveBytes(int index);

  // repeated string init = 4;
  /**
   * <code>repeated string init = 4;</code>
   *
   * <pre>
   * Definition of functions used to report module contents and
   * function calls.  Will be added to the start of the app's main
   * module.
   * </pre>
   */
  java.util.List<java.lang.String>
  getInitList();
  /**
   * <code>repeated string init = 4;</code>
   *
   * <pre>
   * Definition of functions used to report module contents and
   * function calls.  Will be added to the start of the app's main
   * module.
   * </pre>
   */
  int getInitCount();
  /**
   * <code>repeated string init = 4;</code>
   *
   * <pre>
   * Definition of functions used to report module contents and
   * function calls.  Will be added to the start of the app's main
   * module.
   * </pre>
   */
  java.lang.String getInit(int index);
  /**
   * <code>repeated string init = 4;</code>
   *
   * <pre>
   * Definition of functions used to report module contents and
   * function calls.  Will be added to the start of the app's main
   * module.
   * </pre>
   */
  com.google.protobuf.ByteString
      getInitBytes(int index);

  // optional string app_name_setter = 5;
  /**
   * <code>optional string app_name_setter = 5;</code>
   *
   * <pre>
   * name of function(&lt;string&gt;);
   * used to inform the harness about the app name
   * </pre>
   */
  boolean hasAppNameSetter();
  /**
   * <code>optional string app_name_setter = 5;</code>
   *
   * <pre>
   * name of function(&lt;string&gt;);
   * used to inform the harness about the app name
   * </pre>
   */
  java.lang.String getAppNameSetter();
  /**
   * <code>optional string app_name_setter = 5;</code>
   *
   * <pre>
   * name of function(&lt;string&gt;);
   * used to inform the harness about the app name
   * </pre>
   */
  com.google.protobuf.ByteString
      getAppNameSetterBytes();
}
