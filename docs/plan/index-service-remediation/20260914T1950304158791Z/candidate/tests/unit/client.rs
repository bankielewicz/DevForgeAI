use super::*;

#[tokio::test]
async fn async_frame_writes_enforce_limits_before_sending_bytes() {
    for bytes in [vec![], vec![0; 5]] {
        let mut output = Vec::new();
        assert_eq!(
            write_frame(&mut output, &bytes, 4).await.unwrap_err().code,
            ErrorCode::InvalidArgument
        );
        assert!(output.is_empty());
    }
    assert_eq!(
        transport(std::io::Error::from(std::io::ErrorKind::PermissionDenied)).code,
        ErrorCode::AccessDenied
    );
    let (mut writer, reader) = tokio::io::duplex(4);
    drop(reader);
    assert_eq!(
        write_frame(&mut writer, b"data", 4).await.unwrap_err().code,
        ErrorCode::ServiceUnavailable
    );
}
